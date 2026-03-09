from aiogram.fsm.state import State, StatesGroup


class BotStates(StatesGroup):
    start = State()
    add_document = State()