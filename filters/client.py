from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message
import datetime

from utils.check_sub import check_subscribe
from utils.json import read_json
from config_data.config import config
from config_data.config_load import pay_list
from config_data.create_bot import db


class GPTUserPoorFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        chat_id = update.from_user.id
        date = db.read(chat_id, 'expired_time')

        if date:
            now_date = datetime.date.today()
            date_split = date.split('-')
            expired_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
            # Вычисляем разницу между датами
            delta = expired_date - now_date
            if int(delta.days) < 0:
                db.update(chat_id, 'expired_time', '')
                db.update(chat_id, 'premium_type', '')
                return True
        elif db.read(chat_id, "requests_gpt") <= 0:
            return True
        else:
            return False


class MJUserPoorFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        chat_id = update.from_user.id
        date: str = db.read(chat_id, 'expired_time')

        if date:
            now_date = datetime.date.today()
            date_split = date.split('-')
            expired_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
            # Вычисляем разницу между датами
            delta = expired_date - now_date
            if delta.days < 0:
                db.update(chat_id, 'expired_time', '')
                db.update(chat_id, 'premium_type', '')
                return True
        elif db.read(chat_id, "requests_mj") <= 0:
            return True
        else:
            return False


class PikaLabsSUserPoorFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        chat_id = update.from_user.id

        if db.read(chat_id, "requests_pikalabs") <= 0:
            return True
        else:
            return False


class DeepAIUserPoorFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        chat_id = update.from_user.id
        date: str = db.read(chat_id, 'expired_time_deepai')

        if date:
            now_date = datetime.date.today()
            date_split = date.split('-')
            expired_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
            # Вычисляем разницу между датами
            delta = expired_date - now_date
            if delta.days < 0:
                db.update(chat_id, 'expired_time_deepai', '')
                db.update(chat_id, 'premium_type_deepai', '')
                return True
        elif db.read(chat_id, "requests_deepai") <= 0:
            return True
        else:
            return False


class MJRequestsToday(Filter):
    async def __call__(self, update: Message) -> bool:
        chat_id = update.from_user.id
        premium_type = db.read(update.from_user.id, 'premium_type')
        if premium_type:
            if pay_list[premium_type]['limited_reqs']:
                return db.read(chat_id, 'requests_mj_today') >= config["MJLimitRequestsToday"]
        else:
            return False


class CheckSubFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        return await check_subscribe(update.from_user.id)


class QueryPermissionFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        premium_type = db.read(update.from_user.id, 'premium_type')
        if premium_type:
            return pay_list[premium_type]['menu_prompt']
        else:
            return False


class PromptFromQueryFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        data = read_json(config["PromptChoose"])
        for value in data:
            if update.text == value["prompt"]:
                return True
        return False


class StableModelFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        return db.read(update.from_user.id, "model") == "stable"


class ChatGPTModelFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        return db.read(update.from_user.id, "model") == "chatgpt"


class PikaLabsModelFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        return db.read(update.from_user.id, "model") == "pikalabs"


class DeepAIModelFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        return db.read(update.from_user.id, "model") == "deepai"


class DALLEUserPoorFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        chat_id = update.from_user.id
        print(db.read(chat_id, "requests_dalle"), db.read(chat_id, "requests_deepai"))
        if db.read(chat_id, "requests_dalle") <= 0:
            return True
        else:
            return False


class DALLEModelFilter(Filter):
    async def __call__(self, update: Message) -> bool:
        return db.read(update.from_user.id, "model") == "dalle"
