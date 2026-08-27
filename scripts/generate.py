# ruff: noqa: E501,PERF401
from __future__ import annotations

import argparse
import ast
import copy
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
ERROR_MODEL = re.compile(r"(?:Response|Error)[45]\d\d")


@dataclass(frozen=True)
class Operation:
    operation_id: str
    method_name: str
    resource_tag: str
    resource_attribute: str
    resource_class: str
    http_method: str
    path: str
    summary: str
    return_type: str
    idempotent: bool


def has_header_parameter(
    contract: dict[str, Any], path_item: dict[str, Any], operation: dict[str, Any], name: str
) -> bool:
    parameters = [*path_item.get("parameters", []), *operation.get("parameters", [])]
    for parameter in parameters:
        if "$ref" in parameter:
            parameter = (
                contract.get("components", {})
                .get("parameters", {})
                .get(parameter["$ref"].rsplit("/", 1)[-1], {})
            )
        if parameter.get("in") == "header" and parameter.get("name") == name:
            return True
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the LTESocks Python SDK surface.")
    parser.add_argument("--output-root", type=Path, default=ROOT)
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise SystemExit(f"Expected a mapping in {path}")
    return document


def model_class_name(schema_name: str, generator_config: dict[str, Any]) -> str:
    override = generator_config.get("class_overrides", {}).get(schema_name, {})
    return str(override.get("class_name", schema_name))


def response_type(operation: dict[str, Any], generator_config: dict[str, Any]) -> str:
    if operation.get("operationId") in {"getPortVpn", "downloadPortVpnWithPost"}:
        return "FileDownload"
    responses = operation.get("responses", {})
    for status, response in sorted(responses.items(), key=lambda item: str(item[0])):
        if not str(status).startswith("2"):
            continue
        content = response.get("content", {})
        if not content:
            return "None"
        content_type, media = next(iter(content.items()))
        schema = media.get("schema", {})
        if content_type == "*/*":
            return "None"
        if content_type in {"application/pdf", "application/zip", "application/octet-stream"}:
            return "FileDownload"
        if "$ref" in schema:
            return model_class_name(schema["$ref"].rsplit("/", 1)[-1], generator_config)
        schema_type = schema.get("type")
        if schema_type == "object":
            operation_id = str(operation.get("operationId", "response"))
            class_name = operation_id[0].upper() + operation_id[1:]
            return f"{class_name}Response{status}"
        if schema_type == "array":
            item = schema.get("items", {})
            if "$ref" in item:
                name = model_class_name(item["$ref"].rsplit("/", 1)[-1], generator_config)
                return f"list[{name}]"
            return "list[object]"
        return {"boolean": "bool", "integer": "int", "number": "float", "string": "str"}.get(
            schema_type,
            "object",
        )
    return "None"


def contract_operations() -> tuple[list[Operation], dict[str, Any], dict[str, Any]]:
    contract = load_yaml(ROOT / "openapi/openapi.yaml")
    mapping = load_yaml(ROOT / "openapi/operations.yaml")
    generator_config = load_yaml(ROOT / "openapi/generator.yaml")
    aliases = mapping.get("operations", {})
    resources = mapping.get("resources", {})
    found_ids: set[str] = set()
    operations: list[Operation] = []

    for path, path_item in contract.get("paths", {}).items():
        for http_method, operation in path_item.items():
            if http_method not in HTTP_METHODS:
                continue
            operation_id = operation["operationId"]
            found_ids.add(operation_id)
            tags = operation.get("tags", [])
            if len(tags) != 1 or tags[0] not in resources:
                raise SystemExit(f"Operation {operation_id} has an unmapped resource tag: {tags}")
            if operation_id not in aliases:
                raise SystemExit(f"Operation {operation_id} has no public method mapping.")
            resource = resources[tags[0]]
            operations.append(
                Operation(
                    operation_id=operation_id,
                    method_name=aliases[operation_id],
                    resource_tag=tags[0],
                    resource_attribute=resource["attribute"],
                    resource_class=resource["class_name"],
                    http_method=http_method.upper(),
                    path=path,
                    summary=" ".join(str(operation.get("summary", operation_id)).split()),
                    return_type=response_type(operation, generator_config),
                    idempotent=has_header_parameter(
                        contract, path_item, operation, "Idempotency-Key"
                    ),
                )
            )

    extra = set(aliases) - found_ids
    if extra:
        raise SystemExit(f"Mappings exist for unknown operations: {sorted(extra)}")
    if len(operations) != 28:
        raise SystemExit(f"Expected 28 operations, got {len(operations)}")
    return operations, resources, generator_config


def run_generator(destination: Path) -> None:
    document = load_yaml(ROOT / "openapi/openapi.yaml")
    for path_item in document.get("paths", {}).values():
        for http_method, operation in path_item.items():
            if http_method not in HTTP_METHODS:
                continue
            content = operation.get("requestBody", {}).get("content", {})
            if "application/json" in content:
                operation["requestBody"]["content"] = {
                    "application/json": content["application/json"]
                }
            operation_id = operation.get("operationId")
            responses = operation.setdefault("responses", {})
            for status, response in responses.items():
                if isinstance(response, dict) and "*/*" in response.get("content", {}):
                    media = response["content"]["*/*"]
                    response["content"] = (
                        {} if str(status).startswith("2") else {"application/json": media}
                    )
            if operation_id in {"deletePort", "deletePortWithPost"}:
                responses["200"] = {"description": "Successful operation"}
            if operation_id in {"getPortVpn", "downloadPortVpnWithPost"}:
                responses["200"] = {
                    "description": "ZIP archive",
                    "content": {
                        "application/octet-stream": {
                            "schema": {"type": "string", "format": "binary"}
                        }
                    },
                }
                if "500" in responses:
                    responses["500"]["content"] = {
                        "application/json": {"schema": {"$ref": "#/components/schemas/Error"}}
                    }
            if not any(str(status).startswith("2") for status in responses):
                responses["204"] = {"description": "Reserved operation completed"}
    generator_schema = destination.parent / "generator-openapi.yaml"
    generator_schema.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    subprocess.run(
        [
            "openapi-python-client",
            "generate",
            "--path",
            str(generator_schema),
            "--config",
            str(ROOT / "openapi/generator.yaml"),
            "--meta",
            "none",
            "--output-path",
            str(destination),
            "--fail-on-warning",
        ],
        check=True,
    )


def make_enums_forward_compatible(source: str) -> str:
    marker = "(str, Enum):\n"
    if marker not in source or "def _missing_(" in source:
        return source
    method = (
        "(str, Enum):\n"
        "    @classmethod\n"
        "    def _missing_(cls, value: object):\n"
        "        if not isinstance(value, str):\n"
        "            return None\n"
        "        member = str.__new__(cls, value)\n"
        '        member._name_ = f"UNKNOWN_{value}"\n'
        "        member._value_ = value\n"
        "        return member\n\n"
    )
    return source.replace(marker, method, 1)


def postprocess_generated(generated: Path) -> None:
    for path in generated.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        source = re.sub(
            r"(accept_language:\s*str\s*\|\s*Unset\s*=\s*)[\"']en[\"']",
            r"\1UNSET",
            source,
        )
        source = source.replace("Default: 'en'.", "Defaults to the client language.")
        source = make_enums_forward_compatible(source)
        path.write_text(source, encoding="utf-8")
    subprocess.run(["ruff", "format", str(generated)], check=True)


def find_endpoint(generated: Path, operation_id: str) -> Path:
    module_name = re.sub(r"(?<!^)(?=[A-Z])", "_", operation_id).lower()
    matches = list((generated / "api").glob(f"*/{module_name}.py"))
    if len(matches) != 1:
        raise SystemExit(f"Expected one generated module for {operation_id}, found {len(matches)}")
    return matches[0]


def public_arguments(
    endpoint: Path, renames: dict[str, str] | None = None
) -> tuple[str, list[tuple[str, str]], set[str]]:
    tree = ast.parse(endpoint.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "sync_detailed"
    )
    arguments = copy.deepcopy(function.args)

    positional = arguments.posonlyargs + arguments.args
    renames = renames or {}
    names = [
        (argument.arg, renames.get(argument.arg, argument.arg))
        for argument in positional
        if argument.arg != "client"
    ]
    names.extend(
        (argument.arg, renames.get(argument.arg, argument.arg))
        for argument in arguments.kwonlyargs
        if argument.arg != "client"
    )

    if any(argument.arg == "client" for argument in arguments.args):
        index = next(i for i, argument in enumerate(arguments.args) if argument.arg == "client")
        default_offset = len(arguments.args) - len(arguments.defaults)
        arguments.args.pop(index)
        if index >= default_offset:
            arguments.defaults.pop(index - default_offset)
    if any(argument.arg == "client" for argument in arguments.kwonlyargs):
        index = next(
            i for i, argument in enumerate(arguments.kwonlyargs) if argument.arg == "client"
        )
        arguments.kwonlyargs.pop(index)
        arguments.kw_defaults.pop(index)

    def simplify_union(annotation: ast.expr | None) -> ast.expr | None:
        if annotation is None:
            return None

        members: list[ast.expr] = []

        def flatten(node: ast.expr) -> None:
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                flatten(node.left)
                flatten(node.right)
            else:
                members.append(node)

        flatten(annotation)
        unique: list[ast.expr] = []
        seen: set[str] = set()
        for member in members:
            rendered_member = ast.unparse(member)
            if rendered_member not in seen:
                unique.append(member)
                seen.add(rendered_member)
        result = unique[0]
        for member in unique[1:]:
            result = ast.BinOp(left=result, op=ast.BitOr(), right=member)
        return result

    for argument in [*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs]:
        argument.annotation = simplify_union(argument.annotation)
        argument.arg = renames.get(argument.arg, argument.arg)

    type_names: set[str] = set()
    nodes: list[ast.AST] = [
        *(argument.annotation for argument in arguments.posonlyargs if argument.annotation),
        *(argument.annotation for argument in arguments.args if argument.annotation),
        *(argument.annotation for argument in arguments.kwonlyargs if argument.annotation),
        *arguments.defaults,
        *(default for default in arguments.kw_defaults if default is not None),
    ]
    for node in nodes:
        type_names.update(child.id for child in ast.walk(node) if isinstance(child, ast.Name))

    placeholder = ast.FunctionDef(
        name="placeholder",
        args=arguments,
        body=[ast.Pass()],
        decorator_list=[],
        returns=None,
        type_comment=None,
    )
    ast.fix_missing_locations(placeholder)
    rendered = ast.unparse(placeholder).split(":\n", 1)[0].removeprefix("def placeholder")
    rendered = "(self)" if rendered == "()" else rendered.replace("(", "(self, ", 1)
    return rendered, names, type_names


def render_resource(
    operations: list[Operation],
    generated: Path,
    resource_class: str,
    model_modules: dict[str, str],
) -> str:
    imports: list[str] = []
    methods: list[str] = []
    async_methods: list[str] = []
    type_names: set[str] = set()
    needs_builtins = False

    for operation in sorted(operations, key=lambda item: item.method_name):
        endpoint = find_endpoint(generated, operation.operation_id)
        tag_module = endpoint.parent.name
        endpoint_module = endpoint.stem
        imports.append(
            f"from .._generated.api.{tag_module} import {endpoint_module} as _{operation.operation_id}"
        )
        arguments, names, argument_type_names = public_arguments(endpoint, {})
        type_names.update(argument_type_names)
        type_names.update(
            node.id
            for node in ast.walk(ast.parse(operation.return_type, mode="eval"))
            if isinstance(node, ast.Name)
        )
        passed = ", ".join(f"{original}={public}" for original, public in names)
        comma = ", " if passed else ""
        call_name = "_download" if operation.return_type == "FileDownload" else "_call"
        response_call_name = (
            "_download_with_response"
            if operation.return_type == "FileDownload"
            else "_call_with_response"
        )
        idempotency_argument = ", _idempotent=True" if operation.idempotent else ""
        return_statement = (
            f"return cast({operation.return_type}, self._client.{call_name}(_{operation.operation_id}.sync_detailed{idempotency_argument}{comma}{passed}))"
            if operation.return_type != "None"
            else f"self._client.{call_name}(_{operation.operation_id}.sync_detailed{idempotency_argument}{comma}{passed})\n        return None"
        )
        async_return = (
            f"return cast({operation.return_type}, await self._client.{call_name}(_{operation.operation_id}.asyncio_detailed{idempotency_argument}{comma}{passed}))"
            if operation.return_type != "None"
            else f"await self._client.{call_name}(_{operation.operation_id}.asyncio_detailed{idempotency_argument}{comma}{passed})\n        return None"
        )
        response_type = operation.return_type
        if response_type.startswith("list["):
            response_type = f"builtins.{response_type}"
            needs_builtins = True
        response_return = f"return cast(ApiResponse[{response_type}], self._client.{response_call_name}(_{operation.operation_id}.sync_detailed{idempotency_argument}{comma}{passed}))"
        async_response_return = f"return cast(ApiResponse[{response_type}], await self._client.{response_call_name}(_{operation.operation_id}.asyncio_detailed{idempotency_argument}{comma}{passed}))"
        methods.append(
            f'''    def {operation.method_name}{arguments} -> {operation.return_type}:
        """{operation.summary}"""
        {return_statement}

    def {operation.method_name}_with_response{arguments} -> ApiResponse[{response_type}]:
        """{operation.summary}; include response metadata."""
        {response_return}
'''
        )
        async_methods.append(
            f'''    async def {operation.method_name}{arguments} -> {operation.return_type}:
        """{operation.summary}"""
        {async_return}

    async def {operation.method_name}_with_response{arguments} -> ApiResponse[{response_type}]:
        """{operation.summary}; include response metadata."""
        {async_response_return}
'''
        )

    builtins = {
        "Any",
        "ApiResponse",
        "FileDownload",
        "None",
        "bool",
        "dict",
        "float",
        "int",
        "list",
        "object",
        "str",
    }
    special_imports: list[str] = []
    for name in sorted(type_names - builtins):
        if name in model_modules:
            special_imports.append(f"from .._generated.models.{model_modules[name]} import {name}")
        elif name in {"UNSET", "Unset"}:
            special_imports.append(f"from .._generated.types import {name}")
        elif name == "UUID":
            special_imports.append("from uuid import UUID")
        elif name == "datetime":
            special_imports.append("import datetime")
        else:
            raise SystemExit(f"Unable to import annotation name {name} for {resource_class}.")

    return "\n".join(
        [
            "# Generated by scripts/generate.py; do not edit.",
            "from __future__ import annotations",
            "",
            *(["import builtins", ""] if needs_builtins else []),
            "from typing import Any, cast",
            "",
            "from ..files import FileDownload",
            "from ..response import ApiResponse",
            *special_imports,
            *imports,
            "",
            f"class {resource_class}:",
            "    def __init__(self, client: Any) -> None:",
            "        self._client = client",
            "",
            *methods,
            f"class Async{resource_class}:",
            "    def __init__(self, client: Any) -> None:",
            "        self._client = client",
            "",
            *async_methods,
        ]
    )


def generate_resources(operations: list[Operation], generated: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    exports: list[tuple[str, str]] = []
    grouped: dict[str, list[Operation]] = {}
    model_source = (generated / "models/__init__.py").read_text(encoding="utf-8")
    model_modules = {
        class_name: module_name
        for module_name, class_name in re.findall(r"from \.([\w_]+) import (\w+)", model_source)
    }
    for operation in operations:
        grouped.setdefault(operation.resource_class, []).append(operation)

    for class_name, resource_operations in sorted(grouped.items()):
        module_name = resource_operations[0].resource_attribute
        (destination / f"{module_name}.py").write_text(
            render_resource(resource_operations, generated, class_name, model_modules),
            encoding="utf-8",
        )
        exports.extend([(module_name, class_name), (module_name, f"Async{class_name}")])

    lines = ["# Generated by scripts/generate.py; do not edit."]
    for module_name, class_name in exports:
        lines.append(f"from .{module_name} import {class_name}")
    lines.extend(["", "__all__ = ["])
    lines.extend(f'    "{class_name}",' for _, class_name in exports)
    lines.extend(["]", ""])
    (destination / "__init__.py").write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["ruff", "format", str(destination)], check=True)


def generate_public_models(generated: Path, destination: Path) -> None:
    source = (generated / "models/__init__.py").read_text(encoding="utf-8")
    imports: list[str] = []
    names: list[str] = []
    pattern = re.compile(r"from \.([\w_]+) import (\w+)")
    for module_name, class_name in pattern.findall(source):
        if ERROR_MODEL.search(class_name):
            continue
        imports.append(f"from .._generated.models.{module_name} import {class_name}")
        names.append(class_name)
    destination.mkdir(parents=True, exist_ok=True)
    lines = ["# Generated by scripts/generate.py; do not edit.", *imports, "", "__all__ = ["]
    lines.extend(f'    "{name}",' for name in names)
    lines.extend(["]", ""])
    (destination / "__init__.py").write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["ruff", "format", str(destination)], check=True)


def generate_reference(
    operations: list[Operation], contract: dict[str, Any], destination: Path
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    api_lines = [
        "# API resource reference",
        "",
        "All methods exist on both `Client` and `AsyncClient`; async calls must be awaited.",
        "",
    ]
    grouped: dict[str, list[Operation]] = {}
    for operation in operations:
        grouped.setdefault(operation.resource_attribute, []).append(operation)
    for attribute, resource_operations in sorted(grouped.items()):
        api_lines.extend(
            [f"## `{attribute}`", "", "| Method | HTTP endpoint | Returns |", "| --- | --- | --- |"]
        )
        for operation in sorted(resource_operations, key=lambda item: item.method_name):
            api_lines.append(
                f"| `{operation.method_name}()` | `{operation.http_method} {operation.path}` | `{operation.return_type}` |"
            )
        api_lines.append("")
    (destination / "api.md").write_text("\n".join(api_lines), encoding="utf-8")

    model_lines = [
        "# Model reference",
        "",
        "Models use snake_case attributes and provide `to_dict()` / `from_dict()` helpers.",
        "",
    ]
    for name, schema in sorted(contract.get("components", {}).get("schemas", {}).items()):
        description = " ".join(str(schema.get("description", "")).split())
        model_lines.append(f"- `{name}`" + (f" — {description}" if description else ""))
    model_lines.append("")
    (destination / "models.md").write_text("\n".join(model_lines), encoding="utf-8")


def replace_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)


def main() -> None:
    args = parse_args()
    output_root = args.output_root.resolve()
    operations, _, _ = contract_operations()
    contract = load_yaml(ROOT / "openapi/openapi.yaml")

    with tempfile.TemporaryDirectory(prefix="ltesocks-python-") as temporary:
        generated = Path(temporary) / "_generated"
        run_generator(generated)
        postprocess_generated(generated)
        package_root = output_root / "src/ltesocks_sdk"
        replace_tree(generated, package_root / "_generated")
        generate_public_models(generated, package_root / "models")
        generate_resources(operations, generated, package_root / "resources")
        generate_reference(operations, contract, output_root / "docs/reference")

    print(f"Generated {len(operations)} operations into {output_root}.")


if __name__ == "__main__":
    main()
