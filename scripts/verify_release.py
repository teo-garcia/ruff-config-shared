from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "pyproject.toml").open("rb") as pyproject_file:
        version = tomllib.load(pyproject_file)["project"]["version"]

    tag = os.environ.get("GITHUB_REF_NAME")
    if tag is None:
        tag = next((value for value in sys.argv[1:] if value != "--"), None)
    expected_tag = f"v{version}"

    if tag is None:
        raise RuntimeError("release tag is required")
    if tag != expected_tag:
        raise RuntimeError(f"release tag {tag} does not match {expected_tag}")

    sys.stdout.write(f"release tag {tag} matches package version\n")


if __name__ == "__main__":
    main()
