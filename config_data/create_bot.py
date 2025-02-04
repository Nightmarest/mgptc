from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, Redis
import logging as lg
import aiocron

from config_data.config import config
from database.PostgreSQL import PostgreSQL

lg.basicConfig(level=lg.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")#, filename = config["BotLog"])
redis: Redis = Redis(host='redis', port=6375)
storage: RedisStorage = RedisStorage(redis=redis)
bot: Bot = Bot(token=config["BotToken"], default=DefaultBotProperties(parse_mode='HTML'))
dp: Dispatcher = Dispatcher(storage=storage)
router_client: Router = Router()
router_admin: Router = Router()
db = PostgreSQL()


@aiocron.crontab("0 0 * * *")
async def update_requests():
    db.admin_request("UPDATE clients SET requests_mj_today = 0")

@aiocron.crontab("0 0 1 * *")
async def update_requests_for_depd():
    ai = db.admin_request("SELECT id FROM clients")
    for x in ai:
        status = db.read(x, "requested")
        sd = db.read(x, "requests_mj")
        gpt = db.read(x, "requests_gpt")

        # if status >= 5:
        #     db.update(x, "requests_mj", int(sd) + int(config['MonthlySD']))
        #     db.update(x, "requests_gpt", int(gpt) + int(config['MonthlyGPT']))
        # elif status < 5:
        db.update(x, "requests_mj", int(sd) - int(config['MonthlySD']))
        db.update(x, "requests_gpt", int(gpt) - int(config['MonthlyGPT']))
        # db.update(x, "requested", 0)



