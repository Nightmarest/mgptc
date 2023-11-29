from aiogram.fsm.state import State, StatesGroup


class ClientState(StatesGroup):
    prompt_add = State()
    process = State()
