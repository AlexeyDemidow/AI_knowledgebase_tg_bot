from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

# from handlers.tasks_handler import my_tasks, make_task_done
from utils.states import BotStates

router = Router()


# @router.message(Command("tasks"))
# async def user_tasks(message: Message):
#     user_id = message.from_user.id
#     tasks = await my_tasks(str(user_id))
#
#     if not tasks:
#         await message.answer("Задачи не найдены")
#
#     result_text = "📌 Ваши задачи:\n\n"
#
#     for task in tasks:
#         task_str = (
#             f"🔢 ID: {task['id']}\n"
#             f"📝 Название: {task['title']}\n"
#             f"ℹ️ Описание: {task.get('description', 'нет описания')}\n"
#             f"✅ Статус: {task['status']}\n"
#             "——————\n"
#         )
#         result_text += task_str
#
#     await message.answer(result_text)
#
#
# @router.message(Command("done"))
# async def get_task_id(message: Message, state: FSMContext):
#     await message.answer('Введите ID задачи.')
#     await state.set_state(BotStates.waiting_for_task_id)
#
#
# @router.message(BotStates.waiting_for_task_id)
# async def change_status(message: Message, state: FSMContext):
#     task_id = message.text.strip()
#
#     if not task_id.isdigit():
#         await message.answer("❌ Неверный формат ID. Введите число.")
#     else:
#         result_text = "✅ Статус задачи изменен!\n\n"
#
#         task = await make_task_done(task_id)
#
#         task_str = (
#             f"🔢 ID: {task['id']}\n"
#             f"📝 Название: {task['title']}\n"
#             f"ℹ️ Описание: {task.get('description', 'нет описания')}\n"
#         )
#
#         result_text += task_str
#         await message.answer(result_text)
#
#     await state.clear()