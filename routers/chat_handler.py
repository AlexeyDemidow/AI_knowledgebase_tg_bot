import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_settings import config
from service.api_client import ask_backend, show_docs, add_doc_by_url, add_doc
from utils.states import BotStates

router = Router()


@router.message(F.text == "💬 Обычный чат")
async def set_chat_mode(message: Message, state: FSMContext):

    await state.update_data(chat_mode="chat")
    await message.answer("Режим: 💬 обычный чат")


@router.message(F.text == "📄 Чат по документам")
async def set_doc_mode(message: Message, state: FSMContext):

    await state.update_data(chat_mode="document")
    await message.answer("Режим: 📄 вопросы по документам")
    await message.answer("Выберите документ для работы 📄")

    tg_id = message.from_user.id
    username = message.from_user.username

    response = await show_docs(
        tg_id=str(tg_id),
        username=username
    )

    docs = response.get("docs", [])

    if not docs:
        await message.answer("📄 У тебя пока нет документов")
        await state.update_data(chat_mode="chat")
        await message.answer("Режим: 💬 обычный чат")
        return

    kb = InlineKeyboardBuilder()

    for doc in docs[:10]:
        kb.button(
            text=f"{doc['id']} - {doc['name']}",
            callback_data=f"doc_{doc['id']}"
        )

    kb.adjust(1)

    await message.answer(
        "📄 Твои документы:",
        reply_markup=kb.as_markup()
    )


@router.message(BotStates.add_document_by_url)
async def handle_url(message: Message, state: FSMContext):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.answer("❌ Отправьте корректную ссылку")
        return

    tg_id = message.from_user.id
    username = message.from_user.username

    url = message.text.strip()

    result = await add_doc_by_url(
        tg_id=tg_id,
        username=username,
        url=url
    )

    if result["success"]:
        await message.answer("✅ Документ по ссылке успешно загружен")
    else:
        await message.answer(f"❌ Ошибка: {result['errorMsg']}")

    await state.clear()


@router.message(F.text, ~F.state(BotStates.add_document_by_url))
async def chat(message: Message, state: FSMContext):
    data = await state.get_data()
    chat_mode = data.get("chat_mode")
    selected_doc = data.get("selected_doc")
    username = message.from_user.username or "unknown"

    if chat_mode == "document" and not selected_doc:
        await message.answer("❗ Сначала выбери документ")
        return

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    response = await ask_backend(
        tg_id=message.from_user.id,
        username=username,
        message=message.text,
        chat_mode=chat_mode,
        doc_id=selected_doc,
    )

    if response.get("success"):
        await message.answer(response["answer"])
    else:
        await message.answer("⚠️ Сервер временно недоступен")


@router.message(F.document)
async def handle_document(message: Message):

    tg_id = message.from_user.id
    username = message.from_user.username

    document = message.document
    file_name = document.file_name

    data = aiohttp.FormData()
    data.add_field("tg_id", str(tg_id))
    data.add_field("username", username if username else "unknown")

    file = await message.bot.get_file(document.file_id)
    file_obj = await message.bot.download_file(file.file_path)

    data.add_field(
        "file",
        file_obj,
        filename=file_name
    )

    if result["success"]:
        await message.answer("✅ Документ успешно загружен")
    else:
        await message.answer(f"❌ Ошибка: {result['errorMsg']}")
