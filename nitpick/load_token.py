# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional

from loguru import logger

LOADING_FILE_ORDER: list[str] = [
    # 1 docker secrets
    "/run/secrets/token",
    # 2 local
    "./token.txt",
]


def load() -> str:
    token_file: Path = _find_token_file()
    logger.info(f"load token file from {token_file}")
    token: str

    buffer: list[str]
    with token_file.open("r") as fp:
        buffer = list(map(lambda x: x.strip(), fp))

    token = buffer[0]
    if len(token) == 0:
        raise FileNotFoundError("load token error")
    logger.success(f"Success to load token: {token}")
    return token


def _find_token_file() -> Path:
    """
    LOADING_FILE_ORDERに記載されいてる順番でファイル存在の有無をチェックし、最初に見つかったファイルパスを返す

    Raises:
        FileNotFoundError: LOADING_FILE_ORDER記載のパスをすべてチェックしたが、存在しなかった

    Returns:
        Path: 最初に見つかったファイル
    """
    ret_path: Optional[Path] = None
    for path in map(Path, LOADING_FILE_ORDER):
        path = path.resolve()
        if not path.exists():
            continue
        if not path.is_file():
            continue

        ret_path = path
        break

    if ret_path is None:
        raise FileNotFoundError("token file is not found.")

    return ret_path
