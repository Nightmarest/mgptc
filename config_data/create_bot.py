from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage, Redis
import logging as lg
import aiocron

from config_data.config import config
from database.PostgreSQL import PostgreSQL

lg.basicConfig(level=lg.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")#, filename = config["BotLog"])
redis: Redis = Redis(host='localhost')
storage: RedisStorage = RedisStorage(redis=redis)
bot: Bot = Bot(token=config["BotToken"], parse_mode='HTML')
dp: Dispatcher = Dispatcher(storage=storage)
router_client: Router = Router()
router_admin: Router = Router()
db = PostgreSQL()


@aiocron.crontab("0 0 * * *")
async def update_requests():
    db.admin_request("UPDATE clients SET requests_mj_today = 0")


