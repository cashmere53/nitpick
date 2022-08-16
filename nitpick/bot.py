# -*- coding: utf-8 -*-

from __future__ import annotations

from discord import Client, Intents, Interaction, Member, Message, Object
from discord.app_commands import CommandTree, command
from loguru import logger

from nitpick.__init__ import __version__

DEV_GUILD: Object = Object(id=195456248232148992)


class NitpickBot(Client):
    def __init__(self, *, intents: Intents) -> None:
        super().__init__(intents=intents)

        self.tree: CommandTree[Client] = CommandTree(self)
        self.tree.add_command(_hello)
        self.tree.add_command(_mute)
        self.tree.add_command(_unmute)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=DEV_GUILD)
        await self.tree.sync()

    async def on_ready(self) -> None:
        logger.info(f"we have logged in as {self.user}. version={__version__}")

    async def on_message(self, message: Message) -> None:
        logger.info(message)


@command(name="hello", description="hello")
async def _hello(interaction: Interaction) -> None:
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")


@command(name="mute", description="mute member")
async def _mute(interaction: Interaction, member: Member) -> None:
    await member.edit(mute=True, deafen=True)
    await interaction.response.send_message(f"{member} is muted and deafened")


@command(name="unmute", description="unmute member")
async def _unmute(interaction: Interaction, member: Member) -> None:
    await member.edit(mute=False, deafen=False)
    await interaction.response.send_message(f"{member} is unmuted and undeafened")
