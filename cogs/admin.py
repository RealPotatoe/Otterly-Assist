import logging
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logger.info(f"Loaded Cog: {self.__cog_name__}")

    @app_commands.command(name="ping", description="Ask the bot for a pong!")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"Pong2! {round(self.bot.latency * 1000)}ms", ephemeral=True
        )

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    @commands.guild_only()
    async def sync(
        self, ctx: Context, guild_id: Optional[int], copy: bool = False
    ) -> None:
        """Syncs the slash commands with the given guild"""

        if guild_id:
            guild = discord.Object(id=guild_id)
        else:
            guild = ctx.guild

        if copy:
            self.bot.tree.copy_global_to(guild=guild)

        commands = await self.bot.tree.sync(guild=guild)
        await ctx.send(f"Successfully synced {len(commands)} commands")

    @sync.command(name="global")
    @commands.is_owner()
    async def sync_global(self, ctx: Context):
        """Syncs the commands globally"""

        commands = await self.bot.tree.sync(guild=None)
        await ctx.send(f"Successfully synced {len(commands)} commands")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
