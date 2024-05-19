from aiogram import Bot, Dispatcher

from src.project.config import settings
from src.services import PaymentService
from src.telegram_bot.handlers import router


async def start_bot(bot: Bot):
    """Выполнение команд сразу после запуска бота."""
    await PaymentService.restore_database_from_file(settings.path_to_db_file)


async def stop_bot(bot: Bot):
    """Выполнение команд непосредственно перед остановкой бота."""
    await bot.session.close()


async def init_bot() -> None:
    """
    Инициализация бота и диспетчера.
    :return: None.
    """
    bot = Bot(token=settings.bot_token)

    dp = Dispatcher()

    dp.include_router(router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

