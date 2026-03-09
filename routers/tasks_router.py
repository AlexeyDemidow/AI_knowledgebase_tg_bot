import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_settings import config
from handlers.tasks_handler import ask_backend
from utils.states import BotStates

router = Router()

@router.message()
async def chat(message: Message, state: FSMContext):

    response = await ask_backend(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        message=message.text
    )

    await message.answer(response["answer"])
    await state.set_state(BotStates.start)