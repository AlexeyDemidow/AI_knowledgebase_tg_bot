import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_settings import config
from handlers.tasks_handler import ask_backend
from utils.states import BotStates

router = Router()

@router.message(F.text)
async def chat(message: Message, state: FSMContext):

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    username = message.from_user.username or "unknown"

    response = await ask_backend(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        message=message.text
    )

    await message.answer(response["answer"])
    await state.set_state(BotStates.start)