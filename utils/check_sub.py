import aiohttp

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config_data.create_bot import bot
from config_data.config import config
from utils.func import report
from utils.json import update_json, read_json


# удаление элемента из листа каналов
def remove_channel(channel_id):
    channels: dict = read_json(config["CheckSub"])
    for channel in channels:
        if channel['id'] == channel_id:
            channels.remove(channel)
            update_json(config["CheckSub"], channels)
            return channel["first_name"], channel["url"], channel["is_bot"]
    return False


# добавление элемента в лист каналов
def add_channnel(channel_id, first_name, url, is_bot, token = None, skip = False):
    channels: dict = read_json(config["CheckSub"])
    channels.append({"id": channel_id,
                     "first_name": first_name,
                     "url": url,
                     "is_bot": is_bot,
                     "token": token,
                     "skip": skip})
    update_json(config["CheckSub"], channels)


# Клавиатура для проверки подписки
def gen_keyboard():
    channels: dict = read_json(config["CheckSub"])
    keyboard_list = []
    for curr in channels:
        text = f"{curr['first_name']} (нажать /start)" if curr["is_bot"] else curr['first_name']
        subscribe = InlineKeyboardButton(text= text, url=curr['url'])
        keyboard_list.append([subscribe])
    keyboard_list.append([InlineKeyboardButton(text="✅ Я подписался!", callback_data= f"subcheck")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


# проверка на бота
async def check_bot(bot_token, user_id):
    api_url = f"https://api.telegram.org/bot{bot_token}/getChat"
    params = {'chat_id': user_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            data = await response.json()
            if data['ok']:
                return True
            else:
                return False


# проверка на (блуд) подписку
async def check_subscribe(user_id) -> bool:
    if user_id in config["AdminList"]:
        return False
    channels: dict = read_json(config["CheckSub"])
    try:
        for curr in channels:
            if curr["skip"]:
                continue
            if curr["is_bot"]:
                if not await check_bot(curr["token"], user_id):
                    return True
                else:
                    continue
            else:
                x = await bot.get_chat_member(user_id = user_id, chat_id = curr["id"])
                if x.status not in ["member", "creator", "administrator"]:
                    return True
    except Exception as e:
        await report(f"<b>Проблема с ОП❗️</b>: <code>{str(e)}</code>", config["AdminList"])
    return False


async def c_listener(call: CallbackQuery):
    if not await check_subscribe(call.message.chat.id):
        await call.answer("❗️")
        await bot.send_message(call.message.chat.id, "❗️ Вы не подписались!", reply_markup=gen_keyboard())
        return
    await call.answer("✅")
    await call.message.answer('<b>✅ Вы подписаны!</b>\n\n'
                              '<i>ℹ️ Повторите пожалуйста свой запрос.</i>')