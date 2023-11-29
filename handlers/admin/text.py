from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config_data.config import config
from handlers.admin.state import AdminState
from utils.json import read_json, update_json
from utils.func import get_text
from handlers.admin.keyboard import kb


async def text_call_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state()
    step = call.data.split(":")[1]
    langs_admin = read_json(config["LangsAdmin"])
    section = langs_admin["text"][step]

    await call.message.edit_text(
        text=f"<b>✏️ Выбран раздел <code>{section}</code></b>\n\n"
             f"{get_text(f'text.{step}')}",
        reply_markup=kb.text_call_handler(step)
    )


async def update_text(call: CallbackQuery, state: FSMContext):
    step = call.data.split(":")[1]
    langs_admin = read_json(config["LangsAdmin"])
    section = langs_admin["text"][step]
    await state.set_state(AdminState.update_text)
    await state.update_data(update_section=step)

    await call.message.edit_text(
        text=f"<b>✏️ Введите новый текст для раздела <code>{section}</code></b>",
        reply_markup=kb.go_back("text")
    )


async def update_text_done(message: Message, state: FSMContext):
    fsm_data = await state.get_data()
    update_section = fsm_data["update_section"]
    langs_admin = read_json(config["LangsAdmin"])
    section_admin = langs_admin["text"][update_section]
    try:
        langs = read_json(config["Langs"])
        langs["text"][update_section] = message.html_text.replace('"', "'")
        update_json(config["Langs"], langs)
    except Exception as e:
        return await message.answer(f"Не смог выполнить по причине: <code>{e}</code>")

    await state.set_state()
    await message.answer(
        text=f"<b>✏️ Раздел <code>{section_admin}</code> успешно обновлён!</b>",
        reply_markup=kb.go_back("text")
    )