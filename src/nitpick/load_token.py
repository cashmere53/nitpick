from pathlib import Path

from loguru import logger


class TokenLoadError(Exception):
    """Error related to token loading."""


LOADING_FILE_ORDER: list[str] = [
    # 1 docker secrets
    "/run/secrets/token",
    # 2 local
    "./token.txt",
]


def load() -> str:
    """
    Load token from a token file.

    Searches for a file in the order defined by LOADING_FILE_ORDER,
    and returns the token read from the first file found.

    Returns:
        str: The loaded token string

    Raises:
        FileNotFoundError: If no token file is found
        TokenLoadError: If the token is empty
    """
    token_file: Path = _find_token_file()
    logger.info(f"load token file from {token_file}")
    token: str

    buffer: list[str]
    with token_file.open("r") as fp:
        buffer = [x.strip() for x in fp]

    if not buffer or not buffer[0]:
        msg = f"Token is empty in file: {token_file}"
        raise TokenLoadError(msg)

    token = buffer[0]
    logger.success(f"Success to load token: {token}")
    return token


def _find_token_file() -> Path:
    """Find the first existing token file from LOADING_FILE_ORDER.

    Checks for the existence of files in the order listed in LOADING_FILE_ORDER
    and returns the path of the first file found.

    Raises:
        FileNotFoundError: If none of the paths listed in LOADING_FILE_ORDER exist.

    Returns:
        Path: The first file found.
    """
    ret_path: Path | None = None
    for path in map(Path, LOADING_FILE_ORDER):
        fullpath: Path = path.resolve()
        if not fullpath.exists():
            continue
        if not fullpath.is_file():
            continue

        ret_path = fullpath
        break

    if ret_path is None:
        msg = "token file is not found."
        raise FileNotFoundError(msg)

    return ret_path
