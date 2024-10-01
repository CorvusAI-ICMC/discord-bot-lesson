import logging

import discord
from discord import app_commands
from discord.ext import commands


logger = logging.getLogger(__name__)


class MainCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info("On ready from the MainCog")

    @commands.command(name="chat")
    async def chat(self, ctx: commands.Context) -> None:
        await ctx.send("Not in the mood right now")

    @commands.hybrid_command(name="subtract")
    @app_commands.describe(a="The first number", b="The second number")
    async def subtract(self, ctx: commands.Context, a: float, b: float) -> None:
        await ctx.send(f"The difference is {a - b}!")

    @app_commands.command(name="slash")
    async def slash(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Slash command!")
