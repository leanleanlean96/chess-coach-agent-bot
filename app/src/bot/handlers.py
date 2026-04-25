from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from src.contracts.tool_results import WebSearcher, OpeningStatsProvider, VideoFinder
from src.agent.agent import process_message, clear_history
import traceback


def create_router(
    searcher: WebSearcher,
    stats: OpeningStatsProvider,
    finder: VideoFinder,
) -> Router:
    router = Router()

    @router.message(Command("start"))
    async def cmd_start(message: Message):
        clear_history(message.chat.id)
        await message.answer(
            "Привет! Я помогу подобрать шахматный дебют 🎯\n\n"
            "Напиши название дебюта или свой рейтинг и цвет фигур.",
        )

    @router.message(Command("help"))
    async def cmd_help(message: Message):
        await message.answer(
            "Что я умею:\n\n"
            "♟ Подобрать дебют под твой рейтинг и цвет фигур\n"
            "📊 Показать статистику дебюта из Lichess\n"
            "🎥 Найти обучающее видео на YouTube\n\n"
            "Просто напиши свой рейтинг и цвет фигур — я сделаю остальное.",
            "Задавай любой вопрос по шахматам - я помогу!",
        )

    @router.message(F.text)
    async def handle_text(message: Message):
        await message.bot.send_chat_action(message.chat.id, "typing")
        try:
            response = await process_message(
                message.text,
                message.chat.id,
                searcher,
                stats,
                finder,
            )
        except TelegramBadRequest:
            traceback.print_exc()
            response = "Произошла ошибка. Попробуй ещё раз."

        try:
            await message.answer(response, parse_mode="Markdown")
        except Exception as e:
            await message.answer(response, parse_mode=None)

    @router.message(Command("reset"))
    async def cmd_reset(message: Message):
        clear_history(message.chat.id)
        await message.answer("История очищена. Начнём заново!")

    return router
