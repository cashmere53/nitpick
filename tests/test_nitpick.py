# -*- coding: utf-8 -*-

from pathlib import Path

from nitpick import __version__


def test_version() -> None:
    # read pyproject.toml file
    pyproject: Path = Path("./pyproject.toml")
    version_string: str = ""
    with pyproject.open("r", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith("version"):
                version_string = line.lstrip("version =").rstrip().strip('"')
                break

    assert __version__ == version_string
