<div align="center">

# teo-ruff-config-shared

**Shared Ruff configuration for consistent Python linting and formatting**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/teo-ruff-config-shared?color=blue)](https://pypi.org/project/teo-ruff-config-shared)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Part of the [@teo-garcia/templates](https://github.com/teo-garcia/templates) ecosystem

</div>

---

## Settings

| Setting | Value |
| --- | --- |
| **Target** | Python 3.12+ |
| **Line length** | 120 |
| **Quote style** | Double |
| **Rule sets** | E, W, F, I, N, UP, B, S, A, C4, DTZ, T20, SIM, RUF |
| **tests/** | S101 ignored |

---

## Requirements

- Python 3.12+
- Ruff 0.8+

---

## Usage

Install as a dev dependency:

```bash
uv add --dev teo-ruff-config-shared
```

Get the path to the installed config file:

```bash
uv run teo-ruff-config-path
```

Extend it in your `pyproject.toml`:

```toml
[tool.ruff]
extend = "/path/from/teo-ruff-config-path"
```

For a portable setup, add a Makefile target that generates `ruff.extend.toml` (gitignored):

```makefile
ruff-config:
    @echo extend = \"$(shell uv run teo-ruff-config-path)\" > ruff.extend.toml
```

Then in `pyproject.toml`:

```toml
[tool.ruff]
extend = "ruff.extend.toml"
# framework-specific overrides below
```

Add `ruff.extend.toml` to `.gitignore`.

---

## Related Packages

| Package | Description |
| --- | --- |
| `teo-mypy-config-shared` | mypy type-checking settings |
| `teo-pytest-config-shared` | pytest and coverage settings |

---

## License

MIT

---

<div align="center">
  <sub>Built by <a href="https://github.com/teo-garcia">teo-garcia</a></sub>
</div>
