from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.tasks_handler import show_docs

router = Router()

@router.callback_query(lambda c: c.data.startswith("doc_"))
async def handle_doc(callback: CallbackQuery):
    doc_id = callback.data.split("_")[1]

    await callback.answer()

    kb = InlineKeyboardBuilder()
    kb.button(text="📥 Скачать", callback_data=f"download_{doc_id}")
    kb.button(text="🗑 Удалить", callback_data=f"delete_{doc_id}")
    kb.button(text="⬅️ Назад", callback_data="back_to_docs")
    kb.adjust(2, 1)

    await callback.message.edit_text(
        f"📄 Документ {doc_id}",
        reply_markup=kb.as_markup()
    )


@router.callback_query(lambda c: c.data.startswith("download_"))
async def download_doc(callback: CallbackQuery):
    doc_id = callback.data.split("_")[1]

    await callback.answer()
    await callback.message.answer(f"📥 Скачивание документа {doc_id}")


@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_doc(callback: CallbackQuery):
    doc_id = callback.data.split("_")[1]

    await callback.answer()
    await callback.message.answer(f"🗑 Документ {doc_id} удалён")


@router.callback_query(lambda c: c.data == "back_to_docs")
async def back_to_docs(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    user_name = callback.from_user.username or "unknown"

    response = await show_docs(
        tg_id=str(user_id),
        username=user_name
    )

    docs = response.get("docs", [])

    if not docs:
        await callback.message.edit_text("📄 У тебя пока нет документов")
        return

    kb = InlineKeyboardBuilder()

    for doc in docs[:10]:
        kb.button(
            text=f"{doc['id']} - {doc['name']}",
            callback_data=f"doc_{doc['id']}"
        )

    kb.adjust(1)

    await callback.message.edit_text(
        "📄 Твои документы:",
        reply_markup=kb.as_markup()
    )