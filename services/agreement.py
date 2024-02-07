from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import config_data.config
from utils.func import get_text
from config_data.create_bot import db
import config_data.config
from keyboards.client_kb import kb
from handlers.client import client


async def agreement_check(message: Message):
    # db.read(chatid, "agreement")
    await message.answer(f'{get_text("text.start_agreement", message.from_user.id)}\n\n{config_data.config.config["agreement"]}')

async def agreement_ok(message: Message, state: FSMContext):
    db.update(message.from_user.id, "agreement", True)

    await client.command_start(message, state)
