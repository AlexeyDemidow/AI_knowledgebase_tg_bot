import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_settings import config
from handlers.tasks_handler import ask_backend
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


@router.message(F.text)
async def chat(message: Message, state: FSMContext):

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    username = message.from_user.username or "unknown"

    data = await state.get_data()
    chat_mode = data.get("chat_mode")
    response = await ask_backend(
        tg_id=message.from_user.id,
        username=username,
        message=message.text,
        chat_mode=chat_mode,
    )

    if response.get("success"):
        await message.answer(response["answer"])
    else:
        await message.answer("⚠️ Сервер временно недоступен")

    await state.set_state(BotStates.start)


@router.message(F.document)
async def handle_document(message: Message):

    tg_id = message.from_user.id
    username = message.from_user.username

    document = message.document
    file_name = document.file_name

    # получаем файл

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

    async with aiohttp.ClientSession() as session:
        async with session.post(config.url + 'add_document/', data=data) as resp:
            result = await resp.json()

    if result["success"]:
        await message.answer("✅ Документ успешно загружен")
    else:
        await message.answer(f"❌ Ошибка: {result['errorMsg']}")