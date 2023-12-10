import ast
from datetime import datetime
import logging as lg
from random import randint
from fastapi import FastAPI, Query, Request, Form, status as st, HTTPException
from sqlalchemy import select
from aiogram.types import URLInputFile
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

from database.models import Clients, Temp
from config_data.create_bot import bot, db
from services.payment import cloudpay_api, promo as chpr, cryptobot_api
from keyboards.client_kb import kb
from utils import func


lg.basicConfig(level=lg.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")#, filename=config["WebHookLog"])
app = FastAPI()

# @app.post("/pay/auto/")
# async def webhook(AccountId: Annotated[str, Form()], SubscriptionId: Annotated[str, Form()]):
#  # if SubscriptionId != "":
#      await autoupdate(AccountId)
#
#      return {"code": 0}

@app.post("/pay/success/")
async def webhook(AccountId: str = Form(), InvoiceId: str = Form(), Data: str = Form()):
 # if SubscriptionId != "":
    d = ast.literal_eval(Data)
    lg.info(Data)
    await cloudpay_api.check(InvoiceId, d['buytype'], AccountId)

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
    if status[1] == 0:
        r = {
            "url": status[0],
            "code": status[1],
            "reason": status[2]
        }
        raise HTTPException(status_code=201, detail=r)
    else:
        r = {
            "reason": status[0],
            "code": status[1],
        }
        raise HTTPException(status_code=406, detail=r)


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


@app.post("/neural/stable")
async def stableprocess(req: Request):
    response = await req.json()

    if response["status"] == 'processing':
        return 200

    photo_url: str = response["output"][0].replace("\\", "")
    payload: str = response["track_id"]
    chat_id: int = int(payload.split('_')[0])
    track_id: str = payload.split('_')[1]
    prompt: str = payload.split('_')[2]

    today = datetime.now()
    state = await func.state_with(chat_id)
    fsm_data = await state.get_data()
    parts = photo_url.split('/')
    pic_code = parts[-1].split('.')[0]


    if track_id not in fsm_data["mj_status"]:
        return 200

    await state.set_state()
    await state.update_data(
        mj_status="success"
    )

    sessionmaker = db.conn()
    with sessionmaker() as session:
        with session.begin():
            new_temp = Temp(
                pic_code=pic_code,
                prompt=prompt
            )
            session.merge(new_temp)

            user = session.scalar(
                select(Clients)
                .where(Clients.id == int(chat_id))
            )
            user.requests_mj_today += 1

            if user.requests_mj > 0:
                user.requests_mj -= 1

    await bot.delete_message(
        chat_id=chat_id,
        message_id=fsm_data["wait_msg_id"]
    )

    if fsm_data["action"] == "prompt":
        with suppress(TelegramBadRequest):
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo_url,
                caption=func.get_text("text.mj_after_progress"),
                reply_markup=kb.stable(pic_code)
            )

    elif fsm_data["action"] == "upscale":
        with suppress(TelegramBadRequest):
            await bot.send_document(
                chat_id=chat_id,
                document=URLInputFile(
                    url=photo_url,
                    filename=today.strftime("%Y-%m-%d %H:%M:%S" + ".png")
                ),
                caption=func.get_text("text.mj_after_progress_upscale"),
                reply_markup=kb.stable_menu()
            )

    return 200
