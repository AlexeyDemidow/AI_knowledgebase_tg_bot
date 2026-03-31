from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.keyboards import mode_keyboard
from utils.states import BotStates
from service.api_client import create_user, show_docs

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
    await state.set_state(BotStates.start)


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


@router.message(Command("add_doc_by_url"))
async def cmd_add_doc_by_url(message: Message, state: FSMContext):

    text = (
        "📄 Отправьте ссылку на документ для загрузки.\n\n"
        "Поддерживаются файлы:\n"
        "• PDF\n"
        "• DOCX\n"
        "• TXT"
    )

    await message.answer(text)
    await state.set_state(BotStates.add_document_by_url)


@router.message(Command("show_docs"))
async def cmd_show_docs(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username

    response = await show_docs(
        tg_id=str(user_id),
        username=user_name
    )

    docs = response.get("docs", [])

    if not docs:
        await message.answer("📄 У тебя пока нет документов")
        return

    text = "📄 Твои документы:\n\n"

    kb = InlineKeyboardBuilder()

    for doc in docs[:10]:
        kb.button(
            text=f"{doc['id']} - {doc['name']}",
            callback_data=f"doc_{doc['id']}"
        )

    kb.adjust(1)

    await message.answer(
        text,
        reply_markup=kb.as_markup()
    )