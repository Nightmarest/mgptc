import datetime

from aiogram.types import Message, CallbackQuery

from config_data.create_bot import db
from database.models import Clients
from services import agreement
from utils.func import get_text, check_donate_sub, timeword
from keyboards.client_kb import kb
from config_data.config_load import pay_list



async def profile(message: Message, user: Clients):
    card = user.subid
    auto = None
    if card is not None:
        auto = True
    elif card is None:
        auto = False
    chat_id: int = message.from_user.id


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
    agr = db.read(chat_id, "agreement")
    if agr is False:
        await agreement.agreement_check(message)
    text = f"<b>🌙 Доступно запросов для ChatGPT:</b> {user.requests_gpt}\n" \
               f"<b>🍬 Доступно запросов для StableDiffusion:</b> {user.requests_mj}\n" \
               f"<b>🍬 Доступно запросов для Pika Labs:</b> {user.requests_pikalabs}\n" \
               f"<b>🌇 Доступно запросов для DeepAI:</b> {user.requests_deepai}\n" \
               f"<b>🎈 Доступно запросов для Dall-E:</b> {user.requests_dalle}\n\n" \
               f"<b>⏳ Оставшееся время подпииски:</b> {tmd}\n\n"\
               f"{get_text('text.profile')}"
    await message.answer(
        text=text,
        reply_markup=kb.profile(
            user.premium_type,
            user.course,
            user.voice_answer,
            auto
        )
    )


async def call_profile(call: CallbackQuery, user: Clients):
    chat_id: int = call.from_user.id
    card = user.subid
    auto = None
    if card is not None:
        auto = True
    elif card is None:
        auto = False
    days: int = check_donate_sub(chat_id)
    print(days)

    text = f"<b>🌙 Доступно запросов для ChatGPT:</b> {user.requests_gpt}\n"\
               f"<b>🍬 Доступно запросов для StableDiffusion:</b> {user.requests_mj}\n"\
               f"<b>🍬 Доступно запросов для Pika Labs:</b> {user.requests_pikalabs}\n"\
               f"<b>🌇 Доступно запросов для DeepAI:</b> {user.requests_deepai}\n"\
               f"<b>🎈 Доступно запросов для Dall-E:</b> {user.requests_dalle}\n\n"\
               f"<b>⏳ Оставшееся время подпииски:</b> {db.read(chat_id, 'expired_time')}\n\n"\
               f"{get_text('text.profile')}"
    await call.message.edit_text(
        text=text,
        reply_markup=kb.profile(
            user.premium_type,
            user.course,
            user.voice_answer,
            auto
        )
    )


async def switch_voice_answer(call: CallbackQuery, user: Clients):
    chat_id = call.from_user.id

    if user.voice_answer:
        user.voice_answer = False
    else:
        tariff = user.premium_type
        try:
            if pay_list[tariff]['voiceacess'] is None:
                if pay_list[tariff]['voiceacess'] is True:
                    user.voice_answer = True
                else:
                    await call.answer("❌ Активируйте премиум план с данной привелегией")
            else:
                await call.answer("❌ Активируйте премиум план с данной привелегией")
        except Exception as e:
            await call.answer("❌ Активируйте премиум план с данной привелегией")

    await call_profile(call)
