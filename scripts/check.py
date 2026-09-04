from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "teo_ruff_config_shared"


def executable(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"required executable not found: {name}")
    return path


def run(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=True, text=True)  # noqa: S603


def main() -> None:
    ruff = executable("ruff")
    uv = executable("uv")

    run([ruff, "check", "."])
    run([ruff, "format", "--check", "."])

    with tempfile.TemporaryDirectory(prefix="teo-ruff-consumer-") as temp:
        temp_root = Path(temp)
        dist_dir = temp_root / "dist"
        venv_dir = temp_root / "venv"
        consumer_dir = temp_root / "consumer"

        run(
            [
                uv,
                "build",
                "--wheel",
                "--out-dir",
                str(dist_dir),
                "--python",
                sys.executable,
                "--no-python-downloads",
            ]
        )

        wheels = list(dist_dir.glob("*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"expected one wheel, found {len(wheels)}")
        wheel = wheels[0]

        with ZipFile(wheel) as archive:
            package_files = {name for name in archive.namelist() if name.startswith(f"{PACKAGE}/")}

        expected_package_files = {
            f"{PACKAGE}/__init__.py",
            f"{PACKAGE}/ruff.toml",
        }
        if package_files != expected_package_files:
            raise RuntimeError(f"unexpected wheel package files: {sorted(package_files)}")

        run(
            [
                uv,
                "venv",
                str(venv_dir),
                "--python",
                sys.executable,
                "--no-python-downloads",
            ],
            cwd=temp_root,
        )
        venv_python = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run(
            [
                uv,
                "pip",
                "install",
                "--python",
                str(venv_python),
                str(wheel),
                "--no-python-downloads",
            ],
            cwd=temp_root,
        )

        config_executable = venv_dir / (
            "Scripts/teo-ruff-config-path.exe" if os.name == "nt" else "bin/teo-ruff-config-path"
        )
        config_result = subprocess.run(  # noqa: S603
            [str(config_executable)],
            cwd=temp_root,
            check=True,
            capture_output=True,
            text=True,
        )
        config_path = Path(config_result.stdout.strip()).resolve()
        if not config_path.is_file() or not config_path.is_relative_to(venv_dir.resolve()):
            raise RuntimeError(f"wheel config path is invalid: {config_path}")

        consumer_dir.mkdir()
        shutil.copy2(
            ROOT / "tests/fixtures/consumer/sample.py",
            consumer_dir / "sample.py",
        )
        run([ruff, "check", "--config", str(config_path), "."], cwd=consumer_dir)
        run(
            [ruff, "format", "--check", "--config", str(config_path), "."],
            cwd=consumer_dir,
        )

        bad_fixture = consumer_dir / "bad.py"
        bad_fixture.write_text('print("not allowed")\n', encoding="utf-8")
        bad_result = subprocess.run(  # noqa: S603
            [ruff, "check", "--config", str(config_path), str(bad_fixture)],
            cwd=consumer_dir,
            check=False,
            capture_output=True,
            text=True,
        )
        if bad_result.returncode == 0 or "T201" not in bad_result.stdout:
            raise RuntimeError("installed Ruff config did not reject print")

    sys.stdout.write("ruff wheel consumer smoke ok\n")


if __name__ == "__main__":
    main()
