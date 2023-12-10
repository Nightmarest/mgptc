from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    mail = State()

    link_add = State()
    link_delete = State()

    sub_add_bot_1 = State()
    sub_add_bot_2 = State()
    sub_add_channel_1 = State()
    sub_add_channel_2 = State()
    sub_delete = State()

    update_text = State()


class SubState(StatesGroup):
    inputid = State()

class SubStateReqs(StatesGroup):
    input = State()

class CreatePromo(StatesGroup):
    name = State()
    discount = State()
    uses = State()
    finish = State()

class GiveSub(StatesGroup):
    input = State()
    # vrw = State()