from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.mode_keyboard import mode_keyboard
from utils.states import BotStates
from handlers.tasks_handler import create_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    text = (
        "👋 Добро пожаловать в AI knowledge base! \n\n"
    )
    user_id = message.from_user.id
    user_name = message.from_user.username

    await create_user(tg_id=str(user_id), username=user_name)

    await message.answer(text)
    await state.update_data(chat_mode="chat")

    await message.answer(
        "Выберите режим работы:",
        reply_markup=mode_keyboard
    )
    # await state.set_state(BotStates.start)


@router.message(Command("add_doc"))
async def cmd_add_doc(message: Message, state: FSMContext):

    text = (
        "📄 Отправьте документ для загрузки.\n\n"
        "Поддерживаются файлы:\n"
        "• PDF\n"
        "• DOCX\n"
        "• TXT"
    )

    await message.answer(text)
    await state.set_state(BotStates.add_document)
