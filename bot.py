"""
Telegram Vocabulary Learning Bot
Main entry point
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import config
from storage.json_storage import ensure_directories

# Import all handlers
from handlers import start, learn, test, review, stats, words_4000, settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    
    # Ensure data directories exist
    await ensure_directories()
    
    # Check bot token
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Please set your bot token in config.py or BOT_TOKEN environment variable")
        sys.exit(1)
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()
    
    # Register all routers
    dp.include_router(start.router)
    dp.include_router(learn.router)
    dp.include_router(test.router)
    dp.include_router(review.router)
    dp.include_router(stats.router)
    dp.include_router(words_4000.router)
    dp.include_router(settings.router)
    
    logger.info("Starting Vocabulary Learning Bot...")
    
    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
