# -*- coding: utf-8 -*-

from pathlib import Path


def load() -> str:
    token_file: Path = Path("./token.txt")
    token: str

    buffer: list[str]
    with token_file.open("r") as fp:
        buffer = list(map(lambda x: x.strip(), fp))

    token = buffer[0]
    return token
