import logging

import discord
from discord.ext.commands import Context, errors
from discord.ext.commands.bot import Bot


from .commands import MainCog


logger = logging.getLogger(__name__)


def prefix_finder(bot: Bot, _: discord.Message) -> str:
    return "!bruh "


class TheBot(Bot):
    """A Discord bot that uses the commands through both messages and slash commands."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(prefix_finder, *args, **kwargs)

    async def load(self) -> None:
        await self.add_cog(MainCog(self))

    async def on_ready(self) -> None:
        logger.info(f'Logged in as "{self.user}"')

        # Needed for app commands
        try:
            for guild in self.guilds:
                await self.tree.sync(guild=guild)
        except Exception as e:
            logger.error(f"Error syncing application commands: {e}")

    async def on_message(self, message: discord.Message) -> None:
        # Ignore bots, including ourselves
        if message.author.bot:
            return

        # Log the message as an example
        logger.info(
            f"Received message from {message.author} at {message.guild}#{message.channel}: {message.content}"
        )

        # IMPORTANT: This is needed to make the commands work, when overriding on_message
        await self.process_commands(message)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        logger.info(f"Joined guild {guild}")

        try:
            await self.tree.sync(guild=guild)
        except Exception as e:
            logger.error(f"Error syncing application commands: {e}")

    async def on_command_error(
        self, context: Context, exception: errors.CommandError, /
    ) -> None:
        """Handle errors raised by commands."""

        await super().on_command_error(context, exception)

        if isinstance(exception, errors.CommandNotFound):
            await context.send(f"Command `{context.invoked_with}` not found.")
        elif isinstance(exception, errors.MissingRequiredArgument):
            await context.send(
                f"Argument `{exception.param.name}` is a required argument that is missing."
            )
        else:
            logger.error(f"Unhandled exception: {exception}")
            await context.send("An error occurred while running the command.")
