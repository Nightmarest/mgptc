import json
import random
import logging as lg

import aiohttp
# from services.payment import cloudpay_api, cryptobot_api
from aiogram.types import CallbackQuery, Message
import asyncio
from aiogram.fsm.context import FSMContext
from handlers.admin.state import PromoState
from keyboards.client_kb import kb
from config_data.create_bot import db
from utils.func import get_text, report, current_time, check_donate_sub
from config_data.config import config
from config_data.config_load import pay_list
from config_data.create_bot import bot, dp, db


async def crypto_check_payment(call: CallbackQuery):
    data = call.data.split('_')
    buy_type = data[2]
    track_id = data[3]
    if await cryptobot_api.check(track_id) or call.from_user.id in config["AdminList"]:
        await accrual_requests(call, buy_type)
    else:
        await call.answer("❌Счет не был оплачен!")


async def ym_check_payment(call: CallbackQuery):
    data = call.data.split('_')
    buy_type = data[2]
    track_id = data[3]
    payinfo = await cloudpay_api.check(track_id, buy_type)
    lg.info(payinfo)
    if payinfo is not None:
        await accrual_requests(call, buy_type, payinfo[1], payinfo[2], payinfo[3])
    else:
        await call.answer("❌Счет не был оплачен!")


async def accrual_requests(buy_type, chatid, token=None, invoice=None, subid = None):
    chat_id = chatid

    if pay_list[buy_type]["course"]:
        text = f"<b>💫 Поздравлем! Оформлена {pay_list[buy_type]['message_text']}!</b>\n\n" \
               f"Вы уже сейчас можете пройти наше обучение по <a href='{config['EducationUrl']}'>данной ссылке.</a>\n" \
               f"А чтобы испытать меню промптов, перейдите по кнопке\n<b>{get_text('buts.profile')}!</b>"
    else:
        text = f"<b>💫 Поздравляем! Оформлена {pay_list[buy_type]['message_text']}!</b>"

    course = True if db.read(chat_id, 'course') else pay_list[buy_type]["course"]
    donate = pay_list[buy_type]["callback_text"]
    expired_time = pay_list[buy_type]["expired_time"]
    expired_time = current_time(expired_time)

    requests_gpt = pay_list[buy_type]["requests_gpt"]
    requests_gpt = db.read(chat_id, "requests_gpt") + requests_gpt
    requests_mj = pay_list[buy_type]["requests_mj"]
    requests_mj = db.read(chat_id, "requests_mj") + requests_mj
    requests_pikalabs = pay_list[buy_type]["requests_pikalabs"]
    requests_pikalabs = db.read(chat_id, 'requests_pikalabs') + requests_pikalabs
    requests_deepai = pay_list[buy_type]["requests_deepai"]
    requests_deepai = db.read(chat_id, 'requests_deepai') + requests_deepai
    requests_dalle = pay_list[buy_type]["requests_dalle"]
    requests_dalle = db.read(chat_id, 'requests_dalle') + requests_dalle

    if pay_list[buy_type]["product_type"] == "subscribe":
        if pay_list[buy_type]["type"] == "mj+gpt":
            db.update(chat_id, 'expired_time', expired_time)
            db.update(chat_id, 'premium_type', buy_type)
        elif pay_list[buy_type]["type"] == "zeroscope":
            db.update(chat_id, 'expired_time_pika', expired_time)
            db.update(chat_id, 'premium_type_pika', buy_type)
        else:
            db.update(chat_id, f'expired_time_{pay_list[buy_type]["type"]}', expired_time)
            db.update(chat_id, f'premium_type_{pay_list[buy_type]["type"]}', buy_type)
        if invoice and token is not None:
            db.update(chat_id, 'invoiceid', invoice)
            db.update(chat_id, 'cardtoken', token)
            db.update(chat_id, 'subid', subid)
        else:
            pass

    db.update(chat_id, 'buyer', True)
    db.update(chat_id, 'course', course)
    db.update(chat_id, 'requests_gpt', requests_gpt)
    db.update(chat_id, 'requests_mj', requests_mj)
    db.update(chat_id, 'requests_pikalabs', requests_pikalabs)
    db.update(chat_id, 'requests_deepai', requests_deepai)
    db.update(chat_id, 'requests_dalle', requests_dalle)

    await bot.send_message(chatid, text)

    await report('<b>💫 Поздравляем</b>\n\n'
                    f'Username: '
                    f'ID: <code>{chat_id}</code>\n'
                    f'Куплено: <code>{donate}</code>',
                    config["AdminList"])


async def autoupdate(chat_id):
    buy_type = db.read(chat_id, "premium_type")
    expired_time = pay_list[buy_type]["expired_time"]
    expired_time = current_time(expired_time)
    requests_gpt = pay_list[buy_type]["requests_gpt"]
    requests_gpt = db.read(chat_id, "requests_gpt") + requests_gpt
    requests_mj = pay_list[buy_type]["requests_mj"]
    requests_mj = db.read(chat_id, "requests_mj") + requests_mj
    requests_pikalabs = pay_list[buy_type]["requests_pikalabs"]
    requests_pikalabs = db.read(chat_id, 'requests_pikalabs') + requests_pikalabs
    if pay_list[buy_type]["product_type"] == "subscribe":
        if pay_list[buy_type]['type'] == "zeroscope":
            db.update(chat_id, 'expired_time_pika', expired_time)
            db.update(chat_id, 'premium_type_pika', buy_type)
        else:
            db.update(chat_id, f'expired_time_{pay_list[buy_type]["type"]}', expired_time)
            db.update(chat_id, f'premium_type_{pay_list[buy_type]["type"]}', buy_type)

    db.update(chat_id, 'buyer', True)
    db.update(chat_id, 'requests_gpt', requests_gpt)
    db.update(chat_id, 'requests_mj', requests_mj)
    db.update(chat_id, 'requests_pikalabs', requests_pikalabs)
    promo = db.read(chat_id, "promo")
    db.admin_request(f"UPDATE promo SET used = used + 1 WHERE name '{promo}'")
    db.update(chat_id, "promo", None)



async def crypto_currency(call: CallbackQuery):
    await call.message.edit_text(
        text=get_text('text.premium_crypto'),
        reply_markup=kb.crypto_currency(call.data)
    )


async def choose_pay_crypto(call: CallbackQuery):
    chat_id = call.from_user.id
    data = call.data.split("_")

    payment_type = data[1]
    amount = pay_list[payment_type]["amount"]
    currency = data[2]

    url, track_id = await cryptobot_api.create_payment(str(chat_id), amount, currency)
    callback = f"check_crypto_{payment_type}_{track_id}"

    await call.message.edit_text(
        f'{get_text("text.pay")}\n\n'
        f'ID Оплаты: <code>{track_id}</code>',
        reply_markup=kb.pay(callback, url, amount)
    )


async def choose_pay_ym(call: CallbackQuery):
    chat_id = call.from_user.id
    data = call.data.split("_")

    payment_type = data[1]
    track_id = str(chat_id) +  str(random.randint(1, 99999))
    promo = db.read(chat_id, "promo")
    amount = pay_list[payment_type]["amount"]
    print(promo)
    if promo is not None:
        discount = db.admin_request(f"SELECT * FROM promo WHERE name = '{promo}'")
        print(discount, amount)
        amount = int(amount) - (int(amount) / 100 * int(discount[0][3]))
    payinfo = await cloudpay_api.create_payment(track_id, amount, chat_id, data[1])
    print(data)
    print(track_id)
    callback = f"check_ym_{payment_type}_{track_id}"

    await call.message.edit_text(
        text=f'{get_text("text.pay")}\n\n'
        f'ID Оплаты: <code>{track_id}</code>',
        reply_markup=kb.pay(callback, payinfo, amount)
    )


async def more_about_course(call: CallbackQuery):
    await call.message.edit_text(
        text=get_text('text.premium_course'),
        reply_markup= kb.description_premium("buy-2(skip)", "buy-2")
    )


async def description_premium(call: CallbackQuery):
    buy_type = call.data.split("_")[1]
    type = call.data.split("_")[2]

    await call.message.edit_text(
        text=get_text(f'text.premium_{buy_type}'),
        reply_markup=kb.description_premium(buy_type, type)
    )


async def buy_handler(call: CallbackQuery):
    await call.message.edit_text(
        text=f"<b>🍬 {pay_list[call.data]['message_text']}</b>\n\n"
        f"Ваш ID: <code>{call.from_user.id}</code>\n"
        "Выберите метод оплаты 🍬",
        reply_markup=kb.buy_handler(call.data)
    )


async def call_premium(call: CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    await state.clear()

    days = check_donate_sub(chat_id)
    if days:
        text = f"💫 У вас действует подписка, осталось {days} дней!"
    else:
        text = get_text('text.premium')

    await call.message.edit_text(
        text=text,
        reply_markup=kb.premium()
    )

async def promocodes(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    db.update(chat_id, "promo", None)
    await message.answer("""<i>✨ Введите промокод на покупку, если он имеется </i>""", reply_markup=kb.promostage(), parse_mode='html')
    await state.set_state(PromoState.promo)





async def premium(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    days = check_donate_sub(chat_id)
    promo = message.text


    await state.clear()

    promocode = db.admin_request(f"SELECT * FROM promo WHERE name = '{str(promo)}'")
    print(promocode)
    prinfo = ""

    if promocode is None:
        prinfo = "😔 Такого промокода нет в нашей базе данных"
    else:
        try:
            if int(promocode[0][2]) > int(promocode[0][1]):
                prinfo = "😔 У этого промокода закончились количества активаций!"
            else:
                prinfo = f"😊 Хорошие новости, ваш промокод на сумму {promocode[0][3]}% успешно активирован!"
                db.update(chat_id, "promo", promo)
        except Exception as e:
            prinfo = "😔 Такого промокода нет в нашей базе данных"

    if days:
        text = f"{prinfo}\n\n💫 У вас действует подписка, осталось {days} дней!"
    else:
        text = f"{prinfo}\n\n{get_text('text.premium')}"

    await message.answer(
        text=text,
        reply_markup= kb.premium()
    )


async def disable_autoup(call: CallbackQuery):
    await call.message.edit_text(
        text="""Внимание !

⚡️ При отключении подписки вы потеряйте ваш Премимум доступ к боту и возможность им пользоваться до повторной покупки. Отключить доступ сейчас ?""",
        reply_markup=kb.auto_confirm()
    )

async def subcancel(subid):
        url = 'https://api.cloudpayments.ru/subscriptions/cancel'
        headers = { 'content-type': 'application/json' }
        session = aiohttp.ClientSession()
        subcancel = {
            "Id": subid,
        }

        async with session.post(
                url, data = json.dumps(subcancel), headers = headers,
                auth = aiohttp.BasicAuth(
                    config['CPID'],
                    config['CPKEY']
                    )
                ) as resp:
            response = await resp.json(content_type = None)

            resp.close()
            await session.close()
        return response['Success']
async def disable_autoup_off(call: CallbackQuery):
    await call.message.edit_text(
        text="🕐 Пожалуйста, подождите, пока мы отключаем автопродление...",
    )
    chatid = call.from_user.id
    subid = db.read(chatid, "subid")
    status = await subcancel(subid)
    if status is True:
        cardtoken = None
        invoiceid = None
        db.update(chatid, "cardtoken", cardtoken)
        db.update(chatid, 'invoiceid', invoiceid)
        db.update(chatid, 'subid', None)




        await call.message.edit_text(
            text="😔 Автоподписка отключена!",
            reply_markup=kb.back_to_profile()
        )
    else:
        await call.message.edit_text(
            text="❌ Произошла ошибка при отмене подписки. Пожалуйста, обратитесь к менеджеру.",
            reply_markup=kb.back_to_profile()
        )


async def choose_premium(call: CallbackQuery):
    data = call.data.split(":")[1]

    if data == "zeroscope":
        text=f"<b>🎐Pika Labs</b>\n\n" \
              "<i>Нейросеть которая превращает\n" \
              "ваш текстовый запрос в видео.</i>"
    elif data == "mj+gpt":
        text="⚡️ Выберите срок вашей будущей подписки!"
    elif data == "gpt":
        text="⚡️ Выберите срок вашей будущей подписки!"
    else:
        text = call.message.text

    await call.message.edit_text(
        text=text,
        reply_markup=kb.pay_list_keyboard(data, True)
    )
