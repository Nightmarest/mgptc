import asyncio
import re
import os
import logging as lg
from discum import Client
from discum.gateway.response import Resp
from aiogram import Bot

from utils.func import get_text, state_with
from config_data.create_bot import db
from config_data.config import config


app = Client(token=os.getenv("TOKEN"), log=False)
lg.basicConfig(level=lg.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


async def telegram_process(video_url: str, user_id: int) -> None:
    state = await state_with(user_id)
    await state.set_state()
    fsm_data = await state.get_data()
    if fsm_data["mj_status"] == "success":
        return
    wait_msg_id = fsm_data["wait_msg_id"]
    await state.update_data(mj_status="success")

    bot = Bot(config["BotToken"], parse_mode="HTML")

    try:
        await bot.delete_message(
            chat_id=user_id,
            message_id=wait_msg_id
        )
    except:
        pass

    await bot.send_video(
        chat_id=user_id,
        video=video_url,
        caption=get_text("text.pikalabs_after_progress")
    )

    reqs = db.read(user_id, "requests_pikalabs") - 1
    db.update(user_id, "requests_pikalabs", reqs) if reqs >= 0 else ...

    await state.storage.close()
    await bot.session.close()


@app.gateway.command
def hello_world(resp: Resp):
    if not (resp.event.message or resp.event.message_updated):
        return
    m = resp.parsed.auto()

    if not(m['author']['id'] == "1123673306256650240" and m["attachments"]):
        return

    match = re.search(r'Prompt:(.*?)\s*Author:', m["content"])

    if not match:
        return lg.error(f"NOT FIND PROMPT IN {m['content']}")

    extracted_prompt: str = match.group(1).strip()
    user_id: int = db.search_prompt(extracted_prompt)

    if not user_id:
        return lg.error(f"NOT FIND ID IN {extracted_prompt}")

    db.delete_record(user_id)
    lg.info(f"FIND ID: {user_id}")

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(telegram_process(
            video_url=m["attachments"][0]['url'],
            user_id=user_id
        ))
        loop.close()
    except Exception as e:
        lg.error(f"Error in sending: {e}")

if __name__ == "__main__":
    app.gateway.run(auto_reconnect=True)
