from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import config_data.config
from utils.func import get_text
from config_data.create_bot import db, bot
import config_data.config
from keyboards.client_kb import kb
from handlers.client import client


async def lang_check(message: Message):
    # db.read(chatid, "agreement")
    await message.answer(f'🇷🇺 Выберите язык\n\n🇺🇸 Choose language', reply_markup=kb.choose_lang())

async def qlang_check(q: CallbackQuery):
    # db.read(chatid, "agreement")
    await q.message.edit_text(f'🇷🇺 Выберите язык\n\n🇺🇸 Choose language', reply_markup=kb.choose_lang())

async def setlang(q: CallbackQuery):
    l = q.data.split(":")[1]
    db.update(q.from_user.id, "lang", l)
    m = await q.message.edit_text(get_text("text.InstallingLang", q.from_user.id))
    await bot.delete_message(q.from_user.id, m.message_id)
    await q.message.answer(get_text("text.InstalledLang", q.from_user.id), reply_markup=kb.langinstalled(q.from_user.id))