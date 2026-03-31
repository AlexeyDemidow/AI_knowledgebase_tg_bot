import asyncio
import logging

from aiogram import Bot, Dispatcher

from routers import chat_handler, commands_handler, callbacks_handler
from routers.signals_handler import start_bot, stop_bot
from utils.commands import set_commands
from bot_settings import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


async def main():
    dp.startup.register(start_bot)
    dp.include_routers(
        commands_handler.router,
        chat_handler.router,
        callbacks_handler.router,
    )

    dp.shutdown.register(stop_bot)
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())