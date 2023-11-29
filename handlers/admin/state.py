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

class PromoState(StatesGroup):
    promo = State()