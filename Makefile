PYTHON ?= python3

.PHONY: build check verify-release

check:
	uv sync --locked --python "$(PYTHON)" --no-python-downloads
	uv run --no-sync --python "$(PYTHON)" --no-python-downloads python scripts/check.py

build:
	uv build --python "$(PYTHON)" --no-python-downloads

verify-release:
	uv run --no-sync --python "$(PYTHON)" --no-python-downloads python scripts/verify_release.py
