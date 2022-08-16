# -*- coding: utf-8 -*-

from discord import Client, Intents

from nitpick.bot import NitpickBot
from nitpick.load_token import load


def main() -> None:
    intents: Intents = Intents.default()
    client: Client = NitpickBot(intents=intents)

    client.run(load())


if __name__ == "__main__":
    main()
