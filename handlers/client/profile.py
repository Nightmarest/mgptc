import datetime

import pymongo
from aiogram.types import Message, CallbackQuery

from config_data.config import config
from config_data.create_bot import db
from database.models import Clients
from services import agreement
from utils.func import get_text, check_donate_sub, timeword
from keyboards.client_kb import kb
from config_data.config_load import pay_list



async def profile(message: Message, user: Clients):
    chat_id: int = message.from_user.id

    autov2 = False

    days: int = check_donate_sub(chat_id)
    date = db.read(chat_id, 'expired_time')
    tmd = ""
    if date is None:
        tmd = "Неизвестно"
    elif date == "":
        tmd = "Неизвестно"
    else:
        now_date = datetime.date.today()
        date_split = date.split('-')
        expired_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        # Вычисляем разницу между датами
        delta = expired_date - now_date
        tmd = timeword(delta.days)
    # if days:
    #     text = get_text('text.profile')
    # else:
    pm = db.read(chat_id, "premium_type")
    pmreqs = ""
    mjreqs = ""
    if pm is not None:
        if pm != "":
            if pay_list[pm]['infinity'] is True:
                pmreqs = 'Безлимит'
                mjreqs = 'Безлимит'
            else:
                pmreqs = user.requests_gpt
                mjreqs = user.requests_mj
        else:
            pmreqs = user.requests_gpt
            mjreqs = user.requests_mj

    else:
        pmreqs = user.requests_gpt
        mjreqs = user.requests_mj

    premium_type = db.read(chat_id, "premium_type")
    premium_type_deepai = db.read(chat_id, "premium_type_deepai")
    premium_type_pika = db.read(chat_id, "premium_type_pika")

    if premium_type == "":
        txt_premium_type = "Не куплено"
    elif premium_type is None:
        txt_premium_type = "Не куплено"
    else:
        txt_premium_type = pay_list[premium_type]['message_text']

    lang = db.read(chat_id, "lang")
    if lang == "ru":
        text = f"🖱️Подписка - {txt_premium_type}\n" \
                    f"⚖️Осталось - {tmd}\n" \
                    f"<b>📱 Ваш TelegramID:</b> <code>{message.from_user.id}</code>\n\n" \
                    f"<i>Запросы:</i>\n\n" \
                    f"🦋stable diffusion: {pmreqs}\n" \
                    f"📘chatgpt 4: {pmreqs}\n"\
                    f"🧢pika labs: {user.requests_pikalabs}\n" \
                    f"🌑deep ai: {user.requests_deepai}\n"
    elif lang == "en":
        text = f"🖱Subscription - {txt_premium_type}\n" \
               f"⚖️Time of end - {tmd}\n" \
               f"<b>📱 Telegram ID:</b> <code>{message.from_user.id}</code>\n\n" \
               f"<i>Requests:</i>\n\n" \
               f"🦋stable diffusion: {pmreqs}\n"\
               f"📘chatgpt 4: {pmreqs}\n"\
               f"🧢pika labs: {user.requests_pikalabs}\n" \
               f"🌑deep ai: {user.requests_deepai}\n"
    await message.answer(
        text=text,
        reply_markup=kb.profile(
            user.premium_type,
            user.course,
            user.voice_answer,
            True,
            autov2,
            chat_id,
        )
    )


async def call_profile(call: CallbackQuery, user: Clients):
    chat_id: int = call.from_user.id


    autov2 = False


    card = user.subid
    auto = None
    if card is not None:
        auto = True
    elif card is None:
        auto = False
    days: int = check_donate_sub(chat_id)
    date = db.read(chat_id, 'expired_time')
    tmd = ""
    if date is None:
        tmd = "Неизвестно"
    elif date == "":
        tmd = "Неизвестно"
    else:
        now_date = datetime.date.today()
        date_split = date.split('-')
        expired_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        # Вычисляем разницу между датами
        delta = expired_date - now_date
        tmd = timeword(delta.days)
    pm = db.read(chat_id, "premium_type")
    pmreqs = ""
    if pm is not None:
        if pm != "":
            if pay_list[pm]['infinity'] is True:
                pmreqs = 'Безлимит'
            else:
                pmreqs = user.requests_gpt
        else:
            pmreqs = user.requests_gpt
    else:
        pmreqs = user.requests_gpt


    premium_type = db.read(chat_id, "premium_type")
    premium_type_deepai = db.read(chat_id, "premium_type_deepai")
    premium_type_pika = db.read(chat_id, "premium_type_pika")

    if premium_type == "":
        txt_premium_type = "Не куплено"
    elif premium_type is None:
        txt_premium_type = "Не куплено"
    else:
        txt_premium_type = pay_list[premium_type]['message_text']
    lang = db.read(chat_id, "lang")
    if lang == "ru":
        text = f"🖱️Подписка - {txt_premium_type}\n" \
                    f"⚖️Осталось - {tmd}\n" \
                    f"<b>📱 Ваш TelegramID:</b> <code>{call.from_user.id}</code>\n\n" \
                    f"<i>Запросы:</i>\n\n" \
                    f"🦋stable diffusion: {pmreqs}\n" \
                    f"📘chatgpt 4: {pmreqs}\n"\
                    f"🧢pika labs: {user.requests_pikalabs}\n" \
                    f"🌑deep ai: {user.requests_deepai}\n"
    elif lang == "en":
        text = f"🖱️Default - {txt_premium_type}\n" \
               f"⚖️English - {tmd}\n" \
               f"<b>📱 Telegram ID:</b> <code>{call.from_user.id}</code>\n\n" \
               f"<i>Subject:</i>\n\n" \
               f"🦋stable broadcast: {pmreqs}\n"\
               f"📘chatgpt 4: {pmreqs}\n"\
               f"🧢pika labs: {user.requests_pikalabs}\n" \
               f"🌑deep ai: {user.requests_deepai}\n"
                # f"📙dalle 3: {user.requests_dalle}\n"
    await call.message.edit_text(
        text=text,
        reply_markup=kb.profile(
            user.premium_type,
            user.course,
            user.voice_answer,
            auto,
            autov2,
            chat_id
        )
    )


async def switch_voice_answer(call: CallbackQuery, user: Clients):
    chat_id = call.from_user.id

    if user.voice_answer:
        user.voice_answer = False
    else:
        tariff = user.premium_type
        try:
            if pay_list[tariff]['voiceaccess'] is None:
                if pay_list[tariff]['voiceaccess'] is True:
                    user.voice_answer = True
                else:
                    await call.answer("❌ Активируйте премиум план с данной привелегией")
            else:
                await call.answer("❌ Активируйте премиум план с данной привелегией")
        except Exception as e:
            await call.answer("❌ Активируйте премиум план с данной привелегией")

    await call_profile(call, user)
