import os
import logging

import dotenv
import discord

from bot import run_bot_explicit


logger = logging.getLogger(__name__)

DISCORD_TOKEN_ENV = "DISCORD_TOKEN"


def setup_logging() -> None:
    log_format = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S %z"
    discord.utils.setup_logging(
        level=logging.INFO,
        formatter=logging.Formatter(fmt=log_format, datefmt=date_format),
    )


def main() -> None:
    """Entrypoint for the bot"""
    setup_logging()

    logger.info("Starting up...")

    has_dotenv = dotenv.load_dotenv()
    if has_dotenv:
        logger.info("Loaded .env file")

    disc_token = os.environ.get(DISCORD_TOKEN_ENV)
    if disc_token is None:
        logger.error("No token found in environment")
        exit(1)

    logger.info(f'Token found in environment, token="...{disc_token[-3:]}"')

    run_bot_explicit(disc_token)
