import asyncio
from aiogram import Bot, Dispatcher

from src.core.config import config
from src.tools.web_search import TavilyWebSearcher
from src.tools.opening_stats import LichessStatsProvider
from src.tools.video_search import YouTubeVideoFinder
from src.bot.handlers import create_router


async def main():

    searcher = TavilyWebSearcher()
    stats = LichessStatsProvider()
    finder = YouTubeVideoFinder()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    dp.include_router(create_router(searcher, stats, finder))

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
