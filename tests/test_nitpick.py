import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib as tl
else:
    import tomli as tl


def test_version() -> None:
    import nitpick  # noqa: PLC0415

    pyproject_file = Path("./pyproject.toml")
    with pyproject_file.open("rb") as fp:
        parsed_content = tl.load(fp)

    correct_version = parsed_content["project"]["version"]
    assert nitpick.__version__ == correct_version
