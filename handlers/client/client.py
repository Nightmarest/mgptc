from aiogram.types import Message, CallbackQuery, ChatMemberUpdated, KeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

import logging as lg

from services import agreement
from services.select_lang import lang_check
from utils.func import get_text, report, clean
from utils.check_sub import gen_keyboard

from database.models import Clients
from config_data.config import config
from config_data.create_bot import db, bot
from keyboards.client_kb import kb

async def command_start(message: Message, state: FSMContext):
    lg.info(message.text)
    chat_id: int = message.from_user.id
    ref_id: str = clean(message.text[7:])
    name: str = message.from_user.username

    agr = db.read(chat_id, "agreement")


    try:
        if not db.is_new(chat_id):
            pass
        elif ref_id.startswith("ads"):
            db.add_count_ads(ref_id[3:])
            db.recording(chat_id, name, ref_id[3:])
        elif ref_id.isdigit() and ref_id != str(chat_id):
            db.update(ref_id, "people_ref", int(db.read(ref_id, "people_ref")) + 1)
            reqs_gpt: int = db.read(ref_id, "requests_gpt") + config['ReferalTokens']
            reqs_mj: int = db.read(ref_id, "requests_mj") + config['ReferalTokens']
            db.update(ref_id, "requests_gpt", reqs_gpt)
            db.update(ref_id, "requests_mj", reqs_mj)
            await bot.send_message(ref_id, get_text("text.reg_by_ur_link", message.from_user.id))
            db.recording(chat_id, name, ref_id)
        else:
            db.recording(chat_id, name, "")

        await state.set_state()
        await state.update_data(dialog_list = [{"role": "system", "content": ""}])

    except Exception as e:
        lg.error(f"ERROR IN START {e}\nfrom id:{chat_id}")
        await report(f"ERROR IN START\n\n<code>{e}</code>\n\nfrom id:{chat_id}", config["DevList"])
    if db.read(chat_id, "lang") is None:
        await lang_check(message)
        pass
    if agr is False:
        await agreement.agreement_check(message)
        db.update(message.from_user.id, "agreement", True)

        await message.answer_video(
            video=config["VideoUrl"],
            caption=get_text('text.start', message.from_user.id),
            reply_markup=kb.start(chat_id)
        )
    else:
        await message.answer_video(
            video=config["VideoUrl"],
            caption=get_text('text.start', message.from_user.id),
            reply_markup=kb.start(chat_id)
        )


async def user_blocked_bot(event: ChatMemberUpdated, user: Clients):
    user.dead = True


async def user_unblocked_bot(event: ChatMemberUpdated, user: Clients):
    user.dead = False


async def call_warning_user_poor(call: CallbackQuery):
    await call.answer(get_text("text.no_requests", call.from_user.id))


async def warning_user_poor(message: Message):
    await message.answer(get_text("text.no_requests", message.from_user.id))


async def warning_in_progress(message: Message):
    await message.answer(get_text('text.alert_in_progress', message.from_user.id))


async def call_warning_in_progress(call: CallbackQuery):
    await call.answer(get_text("text.call_alert_in_progress", call.from_user.id),
                      show_alert=True)


async def help(message: Message):
    await message.answer(get_text('text.help', message.from_user.id))


async def warning_check_sub(message: Message):
    await message.reply("Чтобы воспользоваться мощью нейросетей, сначала подпишись на каналы! ❤️‍🔥", reply_markup=gen_keyboard())


async def call_warning_check_sub(call: CallbackQuery):
    await call.message.reply("Чтобы воспользоваться мощью нейросетей, сначала подпишись на каналы! ❤️‍🔥", reply_markup=gen_keyboard())


async def limit_requests_today(message: Message):
    await message.answer(get_text('text.limit_request_today', message.from_user.id))


async def call_limit_requests_today(call: CallbackQuery):
    await call.answer()
    await call.message.answer(get_text('text.limit_request_today', call.from_user.id))


async def call_pass(call: CallbackQuery):
    await call.answer()
