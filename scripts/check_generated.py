from __future__ import annotations

import filecmp
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED_PATHS = [
    Path("src/ltesocks_sdk/_generated"),
    Path("src/ltesocks_sdk/models"),
    Path("src/ltesocks_sdk/resources"),
    Path("docs/reference"),
]


def differences(expected: Path, actual: Path) -> list[str]:
    comparison = filecmp.dircmp(expected, actual)
    result = [*(f"only generated: {name}" for name in comparison.left_only)]
    result.extend(f"only repository: {name}" for name in comparison.right_only)
    result.extend(f"changed: {name}" for name in comparison.diff_files)
    result.extend(f"type mismatch: {name}" for name in comparison.funny_files)
    for name, child in comparison.subdirs.items():
        result.extend(f"{name}/{difference}" for difference in differences(child.left, child.right))
    return result


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ltesocks-check-") as temporary:
        output = Path(temporary)
        subprocess.run(
            ["python", str(ROOT / "scripts/generate.py"), "--output-root", str(output)],
            check=True,
        )
        changed: list[str] = []
        for relative in GENERATED_PATHS:
            expected = output / relative
            actual = ROOT / relative
            if not actual.exists():
                changed.append(f"missing: {relative}")
                continue
            changed.extend(f"{relative}/{item}" for item in differences(expected, actual))
        if changed:
            print("Generated files are out of date:")
            print("\n".join(f"- {item}" for item in changed))
            raise SystemExit(1)
    print("Generated files match the pinned OpenAPI schema.")


if __name__ == "__main__":
    main()
