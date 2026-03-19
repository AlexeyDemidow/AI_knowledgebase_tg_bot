from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать работу',
        ),
        BotCommand(
            command='add_doc',
            description='Добавить документ',
        ),
        BotCommand(
            command='show_docs',
            description='Показать документы',
        ),

    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())