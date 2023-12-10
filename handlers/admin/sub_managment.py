import json
import re

import aiohttp
from aiogram.client import session
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import config
from config_data.config_load import pay_list
from handlers.admin.keyboard import kb
from config_data.create_bot import db, bot
from handlers.admin.state import SubState, SubStateReqs, GiveSub
from handlers.client.buy_handler import accrual_requests


# И мой профиль с подписками
# датой и прочим
async def submanage_input(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("🪪 Введите ID пользователя")
    await state.set_state(SubState.inputid)

async def submanage_panel(message: Message, state: FSMContext):
    sticker_file = FSInputFile(config["StickerGPT"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)
    wait_msg_id = wait_msg.message_id

    chatid = message.text

    time = db.read(chatid, "expired_time")
    requests_mj = db.read(chatid, "requests_mj")
    requests_gpt = db.read(chatid, "requests_gpt")
    requests_dalle = db.read(chatid, "requests_dalle")
    requests_deepai = db.read(chatid, "requests_deepai")

    premium_type = db.read(chatid, "premium_type")
    premium_type_deepai = db.read(chatid, "premium_type_deepai")
    premium_type_pika = db.read(chatid, "premium_type_pika")

    print(premium_type_pika, premium_type_deepai, premium_type)

    if time != "" or None:
        txt_time = db.read(chatid, "expired_time")
    else:
        txt_time = "Не найдено"

    if premium_type == "":
        txt_premium_type = "Не найдено"
    elif premium_type is None:
        txt_premium_type = "Не найдено"
    else:
        txt_premium_type = pay_list[premium_type]['message_text']


    if premium_type_deepai == "":
        txt_premium_type_deepai = "Не найдено"
    elif premium_type_deepai is None:
        txt_premium_type_deepai = "Не найдено"
    else:
        txt_premium_type_deepai = pay_list[premium_type_deepai]['message_text']


    if premium_type_pika == "":
        txt_premium_type_pika = "Не найдено"
    elif premium_type_pika is None:
        txt_premium_type_pika = "Не найдено"
    else:
        txt_premium_type_pika = pay_list[premium_type_pika]['message_text']

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=wait_msg_id
    )

    text = f"""🛠️ Информация о подписке пользователя
⏳ Окончание подписки пользователя - {txt_time}    
    
🍬 Запросы StableDiffusion - {requests_mj}
🌙 Запросы GPT - {requests_gpt}
🌇 Запросы DeepAI - {requests_deepai}
🎈 Запросы Dall-E - {requests_dalle}

🍬 Основной тип подписки: {txt_premium_type}
🌇 Тип подписки DeepAI: {txt_premium_type_deepai}
🍬 Тип подписки PikaLabs: {txt_premium_type_pika}

 """
    await message.answer(text, reply_markup=kb.subadmin(chatid))
    await state.clear()



async def submanage_ai(query: CallbackQuery):
    data = query.data
    await query.message.edit_text("Выберите нейросеть", reply_markup=kb.choose_ai(data))



async def submanage_requests_input(query: CallbackQuery, state: FSMContext):
    data = query.data.split(":")
    await state.set_state(SubStateReqs.input)
    print(data)
    await state.update_data(action = data[2], chatid = data[3], ai = data[4])
    await query.message.edit_text("Ввведите кол-во запросов для взаимодействия")

async def submanage_requests_finish(message: Message, state: FSMContext):
    count = message.text
    data = await state.get_data()

    requests = db.read(data['chatid'], f"requests_{data['ai']}")

    if data['action'] == "plus":
        requests = int(count) + int(requests)
        txt = "прибавлено"
    elif data['action'] == "minus":
        requests = max(int(count) - int(requests), 0)
        txt = "снято"

    db.update(data['chatid'], f"requests_{data['ai']}", requests)

    await message.answer(f"Пользователю успешно {txt} {requests} запросов")


async def submanage_attach(query: CallbackQuery):
    data = query.data

    await query.message.edit_text("Выберите нейросеть", reply_markup=kb.choose_ai(data))

async def submanage_attach_choose_tf(query: CallbackQuery):
    data = query.data
    ai = data.split(":")[3]
    print(data)
    builder = InlineKeyboardBuilder()
    if ai == "mj":
        ai = "mj+gpt"
    for i in pay_list:
        if ai == pay_list[i]['type']:
            print(i)
            button_list = [InlineKeyboardButton(text=pay_list[i]['callback_text'], callback_data=f"tf:{i}:{data.split(':')[2]}")]
            builder.add(*button_list)
    await query.message.edit_text("Выберите тариф нейросети", reply_markup=builder.as_markup())

async def submanage_attach_finally(query: CallbackQuery):
    await query.message.edit_text("⚙️ Ожидайте выдачи подписки...")

    tf = query.data.split(":")[1]
    chatid = query.data.split(":")[2]
    print(query.data)
    await accrual_requests(tf, chatid)
    await query.message.edit_text(f"✅ Пользователю успешно выдан тариф {pay_list[tf]['callback_text']}")


async def submanage_remove(query: CallbackQuery):
    chatid = query.data.split(":")[1]

    data = db.admin_request(f"SELECT premium_type, premium_type_pika, premium_type_deepai FROM clients WHERE id = {chatid}")
    avaible_list = []
    print(data)
    kb = InlineKeyboardBuilder()
    for i in data:
        for x in i:
            if x is not None:
                if x != "":
                    avaible_list.append(x)

    if len(avaible_list) >= 1:
        for i in avaible_list:
            button_list = [InlineKeyboardButton(text=pay_list[i]['callback_text'], callback_data=f"subdisable:{i}:{chatid}")]
            kb.add(*button_list)
        kb.adjust(1)
    count = len(avaible_list)
    await query.message.edit_text(f"⚙️ Подписок пользователя: {count}\n\n🤔 Выберите тип отключаемой подписки", reply_markup=kb.as_markup())

async def submanage_remove_finally(query: CallbackQuery):
    data = query.data.split(":")
    subtype = pay_list[data[1]]['dbcolumn']


    db.update(data[2], subtype, "")

    await query.message.edit_text("✅ Подписка успешно отключена!")


async def submanage_recursive_time_give(query: CallbackQuery):
    await query.message.edit_text("⏱️ Выберите тип рассчета времени:", reply_markup=kb.time_choose())


async def submanage_recursive_time_give_count(query: CallbackQuery, state: FSMContext):
    datetime = query.data.split(":")[1]
    data = query.data
    timed = ""
    if datetime == "day":
        timed = "дней"
    elif datetime == "week":
        timed = 'недель'
    elif datetime == "month":
        timed = 'месяцев'
    elif datetime == "year":
        timed = 'лет'

    await query.message.edit_text(f"⏱️ Отправьте количество {timed} для выдачи!")
    await state.set_state(GiveSub.input)
    print(data)
    await state.update_data(time=datetime, calldata=str(data))




async def submanage_recursive_choose(message: Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    await state.clear()
    print(data['calldata'])
    await message.answer("Выберите нейросеть:", reply_markup=kb.choose_ai(f"{data['calldata']}:{data['time']}:{msg}"))

async def submanage_recursive_auto_finally(query: CallbackQuery):
    await query.message.edit_text("⏱️ Начат процесс начисления. Данный процесс может занять до 10 минут.")

    data = query.data.split(":")
    print(data)
    time = 0
    ai = ""
    aitime = ""
    if data[5] == "mj":
        ai = "premium_type"
        aitime = "expired_time"
    elif data[5] == "gpt":
        ai = "premium_type"
        aitime = "expired_time"
    elif data[5] == "pika":
        ai = "premium_type_pika"
        aitime = "expired_time_pika"
    elif data[5] == "deepai":
        ai = "premium_type_deepai"
        aitime = "expired_time_deepai"
    elif data[5] == "dalle":
        ai = "premium_type"
        aitime = "expired_time"

    if data[2] == "day":
        time = 3600
    elif data[2] == "week":
        time = 604800
    elif data[2] == "month":
        time = 2629743
    elif data[2] == "year":
        time = 31556926


    ids = db.admin_request(f"SELECT id, {ai}, {aitime} FROM clients")
    url = 'https://api.cloudpayments.ru/subscriptions/find'
    headers = {'content-type': 'application/json'}
    session = aiohttp.ClientSession()
    subcancel = {
        "accountId": ""
    }
    for i in ids:
        if i[1] is not None:
            if i[1] != "":
                print(i)
                subcancel = {
                    "accountId": i[0]
                }
                url = 'https://api.cloudpayments.ru/subscriptions/find'
                async with session.post(
                        url, data=json.dumps(subcancel), headers=headers,
                        auth=aiohttp.BasicAuth(
                            config['CPID'],
                            config['CPKEY']
                        )
                ) as resp:
                    response = await resp.json(content_type=None)
                    print(response)

                for x in response['Model']:
                    if x['Status'] == "Active":

                        numbers = re.sub(r"\D", "", x['NextTransactionDate'])
                        tariff = db.read(i[0], "premium_type")
                        if tariff != "":
                            if tariff is not None:
                                amount = pay_list[tariff]['amount']
                                if x['Amount'] != amount:
                                    LA_request = {
                                        "Id": x['Id'],
                                        "description":" Подарочные дни. Script made by KNOPPiX",
                                        "StartDate": int(numbers) + time
                                    }
                                    url = 'https://api.cloudpayments.ru/subscriptions/update'


                                    async with session.post(
                                            url, data=json.dumps(LA_request), headers=headers,
                                            auth=aiohttp.BasicAuth(
                                                config['CPID'],
                                                config['CPKEY']
                                            )
                                    ) as resp:
                                        response = await resp.json(content_type=None)
    await query.message.edit_text("✅ Подарочные дни успешно начислены!")

    # db.admin_request(f"SELECT id FROM clients WHERE {pay_list[data]['dbcolumn']} = {data}")