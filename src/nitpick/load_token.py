from pathlib import Path

from loguru import logger


class TokenLoadError(Exception):
    """トークン読み込みに関するエラー."""


LOADING_FILE_ORDER: list[str] = [
    # 1 docker secrets
    "/run/secrets/token",
    # 2 local
    "./token.txt",
]


def load() -> str:
    """
    トークンファイルからトークンを読み込む.

    LOADING_FILE_ORDERで定義された順序でファイルを検索し、
    最初に見つかったファイルからトークンを読み込んで返す。

    Returns:
        str: 読み込まれたトークン文字列

    Raises:
        FileNotFoundError: トークンファイルが見つからない場合
        TokenLoadError: トークンが空の場合
    """
    token_file: Path = _find_token_file()
    logger.info(f"load token file from {token_file}")
    token: str

    buffer: list[str]
    with token_file.open("r") as fp:
        buffer = [x.strip() for x in fp]

    token = buffer[0]
    if len(token) == 0:
        msg = "Token is empty in the file"
        raise TokenLoadError(msg)
    logger.success(f"Success to load token: {token}")
    return token


def _find_token_file() -> Path:
    """
    LOADING_FILE_ORDERに記載されいてる順番でファイル存在の有無をチェックし、最初に見つかったファイルパスを返す.

    Raises:
        FileNotFoundError: LOADING_FILE_ORDER記載のパスをすべてチェックしたが、存在しなかった

    Returns:
        Path: 最初に見つかったファイル
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
