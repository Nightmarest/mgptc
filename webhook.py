import ast
from datetime import datetime
import logging as lg
from random import randint
from typing import Optional

from fastapi import FastAPI, Query, Request, Form, status as st, HTTPException
from sqlalchemy import select
from aiogram.types import URLInputFile
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

from starlette.middleware.cors import CORSMiddleware

import config_data.config
from database.models import Clients, Temp
from config_data.create_bot import bot, db
from services.payment import cloudpay_api, promo as chpr, cryptobot_api
from keyboards.client_kb import kb
from utils import func
from config_data.config_load import pay_list



lg.basicConfig(level=lg.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")#, filename=config["WebHookLog"])
app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/pay/auto/")
# async def webhook(AccountId: Annotated[str, Form()], SubscriptionId: Annotated[str, Form()]):
#  # if SubscriptionId != "":
#      await autoupdate(AccountId)
#
#      return {"code": 0}

@app.post("/pay/success/")
async def webhook(AccountId: str = Form(), TransactionId: str = Form(), Data: Optional[str] = Form(None)):
 # if SubscriptionId != "":
    lg.info("REQUESTED")
    if Data is not None:
        d = ast.literal_eval(Data)
        lg.info(Data)
        await cloudpay_api.check(TransactionId, AccountId, d['buytype'])
    else:
        await cloudpay_api.check(TransactionId, AccountId)

    return {"code": 0}


@app.post("/pay/promocode/")
async def checkpromo(chatid: str = Form(), promo: str = Form()):
 # if SubscriptionId != "":
 #    d = ast.literal_eval(Data)
 #    lg.info(Data)
    status = await chpr.checkpromo(chatid, promo)
    if status[0] == 0:
        r = {
            "code": status[0],
            "reason": status[1],
            "discount": status[2]
        }
        raise HTTPException(status_code=202, detail=r)
    else:
        r = {
            "code": status[0],
            "reason": status[1],
        }
        raise HTTPException(status_code=406, detail=r)



@app.post("/pay/checkout/standart/")
async def standartcheckout(chatid: str = Form(), amount: int = Form(), buytype: str = Form()):
    track_id = str(chatid) +  str(randint(1, 99999))

    status = await cloudpay_api.create_payment(track_id, chatid, amount, buytype)
    lg.error(status)
    if status[1] == 0:
        r = {
            "url": status[0],
            "code": status[1],
            "reason": status[2]
        }
        return r
    else:
        r = {
            "reason": status[0],
            "code": status[1],
        }
        return r


@app.post("/pay/checkout/crypto/")
async def cryptocheckout(chatid: str = Form(), amount: int = Form(), buytype: str = Form()):
    status = await cryptobot_api.create_payment(chatid, amount, buytype)
    if status[1] == 0:
        r = {
            "url": status[0],
            "code": status[1],
            "reason": status[2]
        }
        raise HTTPException(status_code=201, detail=r)
    else:
        r = {
            "reason": status[1],
            "code": status[0],
        }
        raise HTTPException(status_code=406, detail=r)


@app.post("/pay/success/crypto/")
async def cryptosuccess(req: Request):

    lg.info(req.json())
    response = await req.json()
    if response['status'] == "paid":
        await cryptobot_api.check(response["order_id"], response["additional_data"])
    else:
        pass
    return 200


@app.post("/replicate/stable")
async def replicate_dalle(req: Request):
    response = await req.json()

    prompt: str = response["input"]["prompt"]
    user_id: int = response["input"]["user_id"]
    wait_msg_id: int = response["input"]["wait_msg_id"]
    photo_output: str = response["output"][0]
    track_id = func.generate_random_text()
    state = await func.state_with(user_id)

    fsm_data = await state.get_data()

    if fsm_data.get('mj_status') == "success":
        return 200

    await state.set_state()
    await state.update_data(
        mj_status="success"
    )

    sessionmaker = db.conn()
    with sessionmaker() as session:
        with session.begin():
            new_temp = Temp(
                pic_code=track_id,
                prompt=prompt
            )
            session.merge(new_temp)

            user = session.scalar(
                select(Clients)
                .where(Clients.id == int(user_id))
            )
            user.requests_mj_today += 1

            if user.requests_mj > 0:
                user.requests_mj -= 1

    with suppress(TelegramBadRequest):
        await bot.delete_message(
            chat_id=user_id,
            message_id=wait_msg_id
        )

    with suppress(TelegramBadRequest):
        await bot.send_photo(
            chat_id=user_id,
            photo=photo_output,
            caption=func.get_text("text.mj_after_progress"),
            reply_markup=kb.stable(track_id)
        )

    reqs = db.read(user_id, "requests_mj") - 1
    db.update(user_id, "requests_mj", reqs) if reqs >= 0 else ...


@app.post("/replicate/deepai")
async def replicate_deepai(req: Request):
    response = await req.json()

    user_id: int = response["input"]["user_id"]
    wait_msg_id: int = response["input"]["wait_msg_id"]
    photo_output: str = response["output"]

    state = await func.state_with(user_id)

    fsm_data = await state.get_data()

    if fsm_data.get('mj_status') == "success":
        return 200

    await state.set_state()
    await state.update_data(
        mj_status="success"
    )

    await bot.delete_message(
        chat_id=user_id,
        message_id=wait_msg_id
    )

    with suppress(TelegramBadRequest):
        await bot.send_document(
            chat_id=user_id,
            document=photo_output,
            caption=func.get_text("text.deepai_after_progress")
        )

    if fsm_data.get('action') == "upscale":
        reqs = db.read(user_id, "requests_mj") - 1
        db.update(user_id, "requests_mj", reqs) if reqs >= 0 else ...
    else:
        reqs = db.read(user_id, "requests_deepai") - 1
        db.update(user_id, "requests_deepai", reqs) if reqs >= 0 else ...

    await state.update_data(
        action=""
    )
