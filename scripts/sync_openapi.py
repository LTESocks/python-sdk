from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "../../site/docs/openapi.yaml"
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize the canonical public OpenAPI schema.")
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    return parser.parse_args()


def git_commit(source: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(source.parent), "log", "-n", "1", "--format=%H", "--", source.name],
        check=False,
        capture_output=True,
        text=True,
    )
    commit = result.stdout.strip()
    return (
        commit if len(commit) == 40 and all(c in "0123456789abcdef" for c in commit) else "unknown"
    )


def validate(document: dict[str, Any]) -> tuple[int, int]:
    if document.get("info", {}).get("title") != "LTESocks Public API":
        raise SystemExit("Refusing to synchronize a non-public API schema.")
    server = document.get("servers", [{}])[0]
    if server.get("url") != "https://api.ltesocks.io/v2":
        raise SystemExit("The public API server is not https://api.ltesocks.io/v2.")

    paths = document.get("paths", {})
    if any(str(path).startswith("/admin") for path in paths):
        raise SystemExit("The public schema unexpectedly contains admin paths.")
    operations = sum(method in HTTP_METHODS for item in paths.values() for method in item)
    schemas = len(document.get("components", {}).get("schemas", {}))
    if operations != 36 or schemas != 20:
        raise SystemExit(
            f"Unexpected contract size: {operations} operations and {schemas} schemas."
        )
    return operations, schemas


def main() -> None:
    source = parse_args().source.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"OpenAPI source does not exist: {source}")

    content = source.read_bytes()
    document = yaml.safe_load(content)
    if not isinstance(document, dict):
        raise SystemExit("The OpenAPI source is not a mapping.")
    operations, schemas = validate(document)

    destination = ROOT / "openapi/openapi.yaml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()
    metadata = {
        "commit": git_commit(source),
        "operations": operations,
        "repository": "LTESocks/docs",
        "schemas": schemas,
        "sha256": digest,
        "source": source.name,
    }
    (ROOT / "openapi/source.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Synced {operations} operations and {schemas} schemas ({digest[:12]}).")


if __name__ == "__main__":
    main()
