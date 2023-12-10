from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.create_bot import db
from handlers.admin.state import CreatePromo



async def createpromo_start(query: CallbackQuery, state: FSMContext):
    await state.set_state(CreatePromo.name)
    await query.message.edit_text("🔑 Ввведите имя промокода")

async def createpromo_discount(message: Message, state: FSMContext):
    await state.set_state(CreatePromo.discount)

    text = message.text
    await state.update_data(name = text)
    await message.answer("⭐️ Введите скидку промокода (без %)")

async def createpromo_uses(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(discount = text)
    await message.answer("⚠️ Введите максимальное количество промокодов доступных для использования")
    await state.set_state(CreatePromo.uses)


async def createpromo_finally(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()

    db.admin_request(f"INSERT INTO promo (name, uses, used, discount) VALUES ({data['name']}, {text}, 0, {data['discount']})")

    await message.answer(f"Промокод {data['name']} успешно создан!")
    await state.set_state(CreatePromo.finish)
