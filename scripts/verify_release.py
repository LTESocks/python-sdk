from __future__ import annotations

import os
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    tag = os.environ.get("GITHUB_REF_NAME", "")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    expected = f"v{project['version']}"
    if tag != expected:
        raise SystemExit(f"Release tag {tag!r} does not match package version {expected!r}.")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## {project['version']} " not in changelog:
        raise SystemExit("The release version is missing from CHANGELOG.md.")
    print(f"Release metadata is consistent for {tag}.")


if __name__ == "__main__":
    main()
