import json
import logging
import os
from typing import List

import discord
from discord.ext import commands

from database import Database
from models.guild_config import GuildConfig

logger = logging.getLogger(__name__)


def get_prefix(bot, message):
    guild_id = message.guild.id
    db = Database()  # Create a Database instance

    guild_config = db.get_guild_config(guild_id)
    if guild_config:
        return guild_config.prefix
    return "?"


def load_config(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Config file {filename} not found")
    with open(filename, "r") as f:
        return json.load(f)


class MyBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix=get_prefix, intents=intents)

        self.config = load_config("config/config.json")

    async def setup_hook(self) -> None:
        for extension in self.config["initial_extensions"]:
            try:
                await self.load_extension(extension)
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")

    async def on_ready(self) -> None:
        logger.info("🦦 Logged on as {0}!".format(self.user))

        # Add guild configs for all guilds the bot is in
        for guild in self.guilds:
            db = Database()  # Create a Database instance
            if not db.is_guild_config_present(guild.id):
                logger.info(f"Adding guild config for guild ID {guild.id}")
                guild_config = GuildConfig(guild.id, prefix="?")
                db.add_guild_config(guild_config)

    async def on_connect(self) -> None:
        logger.info("🌐 Connected to Discord!")

    async def on_disconnect(self) -> None:
        logger.info("💀 Disconnected from Discord!")

    async def on_resumed(self) -> None:
        logger.info("🔁 Session resumed!")

    async def on_command(self, ctx) -> None:
        logger.info(f"{ctx.author} ran command {ctx.command} in {ctx.guild}")
