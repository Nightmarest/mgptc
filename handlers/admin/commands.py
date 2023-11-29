from aiogram.types import Message, FSInputFile
import sys, os
from config_data.create_bot import db
from utils.func import current_time
from config_data.config import config

bd_table = config["BDTable"]

# Обработчик для команды /проверить
async def check_user(message: Message):
    try:
        user_id = message.text.split(' ')[1]
        reqs = str(db.read(user_id, 'requests'))
        await message.answer(reqs)
    except:
        await message.answer("Такого ID нет или он введен неверно\n\nФормат: /проверить ID")


# Обработчик для команды /увеличить
async def increase_user(message: Message):
    try:
        user_id = message.text.split(' ')[1]
        s = message.text.split(' ')[2]
        if s == "week":
            dt = current_time("week")
            db.update(user_id, 'expired_time', dt)
        elif s == "month":
            dt = current_time("month")
            db.update(user_id, 'expired_time', dt)
        else:
            reqs = int(db.read(user_id, 'requests')) + int(s)
            db.update(user_id, 'requests', reqs)

        await message.answer("Успешно!")
    except Exception as e:
        await message.answer("Такого ID нет или он/сумма введены неверно\n\nФормат: /увеличить ID СУММА")


# Обработчик для команды /уменьшить
async def decrease_user(message: Message):
    try:
        user_id = message.text.split(' ')[1]
        s = message.text.split(' ')[2]
        reqs = int(db.read(user_id, 'requests')) - int(s)
        db.update(user_id, 'requests', reqs)
        await message.answer("Успешно!")
    except:
        await message.answer("Такого ID нет или он/сумма введены неверно\n\nФормат: /уменьшить ID СУММА")


# Обработчик для команды /выгрузка
async def export_users(message: Message):
    with open("handlers/user_ids.txt", "w") as file:
        user_ids = db.get_users()
        for user_id in user_ids:
            file.write(str(user_id[0]) + "\n")
    f = FSInputFile("handlers/user_ids.txt")
    await message.answer_document(f)


# Обработчик для команды /restart
async def restart_bot(message: Message):
    await message.answer('Перезапускаю...')
    python = sys.executable
    os.execl(python, python, *sys.argv)
