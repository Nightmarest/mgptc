from aiogram import Bot
from config_data.config import config



async def send_log(user_id: int, username: str, log: str) -> None:
    bot_inistance = Bot(config[""])