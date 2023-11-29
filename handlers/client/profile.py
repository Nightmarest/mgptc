from aiogram.types import Message, CallbackQuery

from database.models import Clients
from utils.func import get_text, check_donate_sub
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
    if days:
        text = get_text('text.profile')
    else:
        text = f"<b>🌙 Доступно запросов для ChatGPT:</b> {user.requests_gpt}\n" \
               f"<b>🍬 Доступно запросов для Midjourney:</b> {user.requests_mj}\n" \
               f"<b>🍬 Доступно запросов для Pika Labs:</b> {user.requests_pikalabs}\n\n" \
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
    if days:
        text = get_text('text.profile')
    else:
        text = f"<b>🌙 Доступно запросов для ChatGPT:</b> {user.requests_gpt}\n" \
               f"<b>🍬 Доступно запросов для Midjourney:</b> {user.requests_mj}\n" \
               f"<b>🍬 Доступно запросов для Pika Labs:</b> {user.requests_pikalabs}\n\n" \
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
