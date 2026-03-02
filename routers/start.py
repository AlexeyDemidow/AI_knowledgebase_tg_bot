from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.states import BotStates

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    text = (
        "👋 Добро пожаловать в AI knowledge base! \n\n"
    )
    user_id = message.from_user.id
    user_name = message.from_user.username
    await message.answer(text)
    await message.answer(f'Ваш ID: {str(user_id)}')
    await message.answer(f'Ваш юзернейм: {str(user_name)}')
    await state.set_state(BotStates.start)