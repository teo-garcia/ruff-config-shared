from importlib.resources import files
from pathlib import Path
from sys import stdout


def config_path() -> Path:
    return Path(str(files(__package__).joinpath("ruff.toml")))


def _cli() -> None:
    stdout.write(f"{config_path()}\n")
