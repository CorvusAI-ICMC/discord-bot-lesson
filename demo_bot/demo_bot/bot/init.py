import asyncio
import logging
import signal

import discord

from .client import TheBot

logger = logging.getLogger(__name__)


async def create_client() -> discord.Client:
    """Create a new Discord client"""
    # Configure the client intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    # return Client(intents=intents)
    bot = TheBot(intents=intents)

    await bot.load()

    return bot


async def run_bot(token: str) -> None:
    """Entrypoint for the bot"""

    logger.info("Connecting to Discord...")

    client = await create_client()

    try:
        # Run the bot
        # This commands do a lot in the background:
        #   Basically, it will start the asyncio loop and run the bot on it, connecting to Discord
        # This will block the main thread until the bot is shutdown
        client.run(token)
    except Exception as e:
        logger.error(f"Error running bot: {e}")

    logger.info("Bot has shutdown")


def run_bot_explicit(token: str) -> None:
    """
    Entrypoint for the bot, but with explicit asyncio loop.

    You'd usually do this if you want to run the bot alongside
    othe stuff, like an HTTP server.
    """
    try:
        asyncio.run(_run_bot_explicit_task(token))
    except Exception as e:
        logger.error(f"Error running bot: {e}")


async def _run_bot_explicit_task(token: str) -> None:
    """
    Entrypoint for the bot, but with explicit asyncio loop.

    You'd usually do this if you want to run the bot alongside
    othe stuff, like an HTTP server.
    """

    # Create a new event loop
    loop = asyncio.get_event_loop()

    # For notifying the main thread that the bot has shutdown
    shutdown_event = asyncio.Event()

    try:
        client = await create_client()
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        return

    # Create a new task that will run the bot
    bot_task = asyncio.create_task(client.start(token))

    # Create a handler for the shutdown event
    def shutdown_handler(*_) -> None:
        logger.info("Shutting down bot")
        shutdown_event.set()
        bot_task.cancel()

    # Register the shutdown handler
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown_handler)

    # Run the bot
    try:
        await asyncio.wait([bot_task])
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down bot")
        shutdown_handler()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        shutdown_handler()
