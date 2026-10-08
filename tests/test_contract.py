from __future__ import annotations

import asyncio
import hashlib
import importlib
import inspect
import json
import re
from pathlib import Path
from typing import Any

import yaml

from ltesocks_sdk import AsyncClient, Client
from ltesocks_sdk.models import OrderPortsBody, PortStatus

ROOT = Path(__file__).resolve().parents[1]
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def documents() -> tuple[dict[str, Any], dict[str, Any]]:
    contract = yaml.safe_load((ROOT / "openapi/openapi.yaml").read_text())
    mapping = yaml.safe_load((ROOT / "openapi/operations.yaml").read_text())
    return contract, mapping


def test_pinned_contract_metadata_and_operation_map() -> None:
    contract, mapping = documents()
    operations = [
        operation
        for path_item in contract["paths"].values()
        for method, operation in path_item.items()
        if method in HTTP_METHODS
    ]
    assert len(operations) == 36
    assert len(contract["components"]["schemas"]) == 20
    assert {operation["operationId"] for operation in operations} == set(mapping["operations"])
    assert len(mapping["resources"]) == 5

    metadata = json.loads((ROOT / "openapi/source.json").read_text())
    assert metadata["operations"] == 36
    assert metadata["schemas"] == 20
    digest = hashlib.sha256((ROOT / "openapi/openapi.yaml").read_bytes()).hexdigest()
    assert metadata["sha256"] == digest


def test_every_operation_has_sync_async_and_response_facades() -> None:
    contract, mapping = documents()
    checked = 0
    for path_item in contract["paths"].values():
        for method, operation in path_item.items():
            if method not in HTTP_METHODS:
                continue
            resource = mapping["resources"][operation["tags"][0]]
            module = importlib.import_module(f"ltesocks_sdk.resources.{resource['attribute']}")
            sync_class = getattr(module, resource["class_name"])
            async_class = getattr(module, f"Async{resource['class_name']}")
            method_name = mapping["operations"][operation["operationId"]]
            assert not inspect.iscoroutinefunction(getattr(sync_class, method_name))
            assert inspect.iscoroutinefunction(getattr(async_class, method_name))
            assert hasattr(sync_class, f"{method_name}_with_response")
            assert hasattr(async_class, f"{method_name}_with_response")
            checked += 1
    assert checked == 36


def test_client_resources_and_models() -> None:
    sync = Client.anonymous()
    async_client = AsyncClient.anonymous()
    try:
        for attribute in ("user", "ports", "payments", "general"):
            assert hasattr(sync, attribute)
            assert hasattr(async_client, attribute)
    finally:
        sync.close()
        asyncio.run(async_client.close())

    assert OrderPortsBody(plan="plan-id").to_dict()["plan"] == "plan-id"
    assert PortStatus("future-status").value == "future-status"


def test_local_documentation_links_resolve() -> None:
    markdown = [ROOT / "README.md", *(ROOT / "docs").rglob("*.md")]
    missing: list[str] = []
    for document in markdown:
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", document.read_text()):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if relative and not (document.parent / relative).resolve().exists():
                missing.append(f"{document.relative_to(ROOT)} -> {target}")
    assert missing == []
