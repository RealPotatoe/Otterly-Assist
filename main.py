import asyncio
import json
import logging
import logging.handlers
import os
from contextlib import contextmanager

import discord
from dotenv import load_dotenv

from bot import MyBot


@contextmanager
def setup_logging(logs_dir: str):
    logger = logging.getLogger()

    try:
        discord.utils.setup_logging()

        logging.getLogger("database").setLevel(logging.WARNING)
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.getLogger("discord.state").setLevel(logging.WARNING)

        max_bytes = 32 * 1024 * 1024  # 32 MiB
        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(logs_dir, "discord.log"),
            encoding="utf-8",
            maxBytes=max_bytes,
            backupCount=5,
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        yield
    finally:
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)


def main():
    # Load environment variables from .env file
    load_dotenv()

    with setup_logging("logs"):
        asyncio.run(launch_bot())


async def launch_bot():
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        raise ValueError("DISCORD_TOKEN environment variable not set")

    async with MyBot() as bot:
        await bot.start(token)


if __name__ == "__main__":
    main()
