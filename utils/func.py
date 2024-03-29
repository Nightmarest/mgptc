from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from thefuzz import fuzz
import re, asyncio, datetime, aiohttp
import logging as lg
import string, random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from utils.json import read_json
from config_data.config import config, MODELS_STABLE, STYLE_STABLE, FORMAT_STABLE
from config_data.config_load import ban_list
from config_data.create_bot import bot, dp, db


# # Получить текст по коду из бд
# def get_text(code: str, session: Session) -> str:
#     text = session.scalar(
#         select(Language.rus)
#         .where(Language.index == code)
#     )

#     return text


# Получить текст по коду из JSON файла
def get_text(code: str, id: int) -> str:
    lang = db.read(id, "lang")
    langs = read_json(config["Langs"][lang])
    data = code.split(".")
    section = data[0]
    name = data[1]
    return langs[section][name]


def clean(string: str) -> str:
    alnum_spaces = re.sub(r'[^a-zA-Z0-9а-яА-Я -:]', '', string)
    return alnum_spaces.strip()


# Текущая дата
# Now time for box
def current_time(type: str) -> datetime.date:
    current_date = datetime.date.today()
    one_week = datetime.timedelta(weeks=1)
    two_week = datetime.timedelta(weeks=2)
    one_month = datetime.timedelta(days=30)
    three_month = datetime.timedelta(days=90)
    if type == "week":
        future_date = current_date + one_week
    elif type == "two_week":
        future_date = current_date + two_week
    elif type == "month":
        future_date = current_date + one_month
    elif type == "three_month":
        future_date = current_date + three_month
    else:
        future_date = ""
    return future_date


# РАНДОМИЗАТОР ДЛЯ ТОКЕНА
def generate_random_text() -> str:
    letters = string.ascii_letters  # Все буквы алфавита
    random_text = ''.join(random.choice(letters) for _ in range(10))
    return random_text


# Check response
def check_ban_words(response: str) -> str:
    data = response.lower().split(" ")
    for ban_word in ban_list:
        for word in data:
            if fuzz.ratio(ban_word.lower(), word) > 90:
                return ban_word
    return ""


def check_donate_sub(chat_id: int) -> int:
    date = db.read(chat_id, 'expired_time')
    if date:
        now_date = datetime.date.today()
        date_split = date.split('-')
        expired_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        # Вычисляем разницу между датами
        delta = expired_date - now_date
        if int(delta.days) < 0:
            db.update(chat_id, 'expired_time', '')
            return 0
        else:
            return delta.days
    else:
        return 0


async def report(text: str, list_id: list) -> None:
    for chat_id in list_id:
        await bot.send_message(chat_id, text)


async def check_mj_status(
        chat_id: int, track_id: str, request: str,
        wait_msg_id: int, state: FSMContext
    ) -> None:
    await asyncio.sleep(config["MJTime"])
    fsm_data = await state.get_data()
    mj_status = fsm_data['mj_status']
    if track_id in mj_status:
        await bot.send_message(chat_id=chat_id,
                            text=get_text('text.mj_error'))
        lg.error(f'ERROR IN MJ: ID{chat_id}, {request}')
        await state.set_state()
        try:
            await bot.delete_message(chat_id= chat_id, message_id= wait_msg_id)
        except:
            pass


async def state_with(user_id: int) -> FSMContext:
    return FSMContext(
        bot=bot, # объект бота
        storage=dp.storage, # dp - экземпляр диспатчера
        key=StorageKey(
            chat_id=user_id,
            user_id=user_id, # если юзер в ЛС, то user_id=user_id
            bot_id=bot.id))


async def shorten_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://clck.ru/--?url={url}') as response:
            if response.status == 200:
                return await response.text()
            else:
                return url



async def check_photo_nsfw(photo_link: str) -> bool:
    headers = {
        'api-key': config["DeeplToken"]
    }

    data = {
        'image': photo_link
    }

    url = 'https://api.deepai.org/api/nsfw-detector'


    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data) as response:
            data = await response.json()
            if "output" in data:
                return bool(data["output"]["detections"])
            else:
                raise Exception(f"check_photo_nsfw: {data}")


def stable_formatted(element: str) -> str:
    finally_element = ""

    MODELS_TUPLE = []
    for key, value in MODELS_STABLE.items():
        MODELS_TUPLE.append((value.get('first_name'), key))

    stable_list = MODELS_TUPLE + STYLE_STABLE + FORMAT_STABLE

    for stable in stable_list:
        if stable[1] == element:
            finally_element = stable[0]

    return finally_element


def timeword(d=0, h=0, m=0):
    dmy = {'d': int(d), 'h': int(h), 'm': int(m)}
    print(dmy)
    words = {'y': ['лет', 'год', 'года'], 'mouth': ['месяцев', 'месяц', 'месяца'], 'd': ['дней', 'день', 'дня'],
             'h': ['часов', 'час', 'часа'],
             'm': ['минут', 'минута', 'минуты']}

    out = []
    for k, v in dmy.items():
        remainder = v % 10
        if v == 0 or remainder == 0 or remainder >= 5 or v in range(11, 19):
            st = str(v), words[k][0]
        elif remainder == 1:
            st = str(v), words[k][1]
        else:
            st = str(v), words[k][2]

        if int(st[0]) > 0:
            out.append(" ".join(st))
        else:
            pass

    time = " ".join(out)
    return time

async def checksub(chatid):

    if int(db.read(chatid, "presub_requests")) >= 2:
        user_channel_status = await bot.get_chat_member(chat_id='2130320163', user_id=chatid)
        lg.error(user_channel_status.status)
        if user_channel_status.status == "left":
            keyboard_list = []
            keyboard_list.append([InlineKeyboardButton(text="Наш форум", url=config['forumlink'])])
            txt = """Уважаемый пользователь, для продолжения подпишитесь на наш <a href='https://t.me/infoblik'>Канал,</a> где вы можете учиться делать промты, следить за последними реально! интересными новостями, а не теми, что вводят вас в тревогу. 

Так же за подписку вы будете получать <b>подарком</b> 5 бесплатных генераций в (sd+chatgpt) в неделю, а за отписку генерации сгорают."""
            await bot.send_message(chat_id=chatid, text=txt, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_list), disable_web_page_preview=True)
            if int(db.read(chatid, "gift")) == 1:
                db.update(chatid, "requests_gpt", int(db.read(chatid, "requests_gpt")) - 5)
                db.update(chatid, "requests_mj", int(db.read(chatid, "requests_mj")) - 5)
                db.update(chatid, "gift", 0)
            return 0
        if int(db.read(chatid, "gift")) == 0:
            db.update(chatid, "requests_gpt", int(db.read(chatid, "requests_gpt")) + 5)
            db.update(chatid, "requests_mj", int(db.read(chatid, "requests_mj")) + 5)
            db.update(chatid, "gift", 1)

            return 1

    elif int(db.read(chatid, "presub_requests")) < 2:
        count = int(db.read(chatid, "presub_requests")) + 1
        print(f"gyyg{count}")
        db.update(chatid, "presub_requests", count)
        return 2



