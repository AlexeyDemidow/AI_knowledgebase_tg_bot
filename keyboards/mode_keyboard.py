from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


mode_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Обычный чат"),
            KeyboardButton(text="📄 Чат по документам")
        ]
    ],
    resize_keyboard=True
)