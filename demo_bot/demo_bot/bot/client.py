import logging
import discord
from discord.ext import commands
from discord.ext.commands import Context, errors
from .commands import MainCog

logger = logging.getLogger(__name__)

def prefix_finder(bot: commands.Bot, _: discord.Message) -> str:
    return "!cmd "  # Prefixo dos comandos

class TheBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def load(self) -> None:
        await self.add_cog(MainCog(self))  # Adiciona o cog

    async def on_ready(self) -> None:
        logger.info(f'Logged in as "{self.user}"')
        await self.load()  # Adiciona o cog
        await self.tree.sync()  # Sincroniza os comandos do aplicativo

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        logger.info(f"Received message: {message.content}")
        await self.process_commands(message)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        logger.info(f"Joined guild {guild}")
        await self.tree.sync(guild=guild)

    async def on_command_error(self, context: Context, exception: errors.CommandError) -> None:
        await super().on_command_error(context, exception)
        if isinstance(exception, errors.CommandNotFound):
            await context.send(f"Command `{context.invoked_with}` not found.")
        elif isinstance(exception, errors.MissingRequiredArgument):
            await context.send(f"Argument `{exception.param.name}` is a required argument that is missing.")
        else:
            logger.error(f"Unhandled exception: {exception}")
            await context.send("Ocorreu um erro ao executar o comando.")


