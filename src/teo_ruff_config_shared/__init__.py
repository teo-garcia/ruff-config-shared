from importlib.resources import files
from pathlib import Path


def config_path() -> Path:
    return Path(str(files(__package__).joinpath("ruff.toml")))


def _cli() -> None:
    print(config_path())
