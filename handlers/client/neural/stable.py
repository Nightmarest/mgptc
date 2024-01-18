import asyncio
import re
import io
import logging as lg
import requests

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, BufferedInputFile
from sqlalchemy.orm import Session
from sqlalchemy import select

from filters.states.state import ClientState
from database.models import Stable, Clients, Temp
from config_data.create_bot import config, bot, db
from keyboards.client_kb import kb

from services.neural.stable import stable_pic
from services.neural.deepai import upscale_photo
from utils.func import check_mj_status, generate_random_text, get_text, clean, checksub
from services.neural.replicate import replicate


async def stable_prompt(message: Message, state: FSMContext, stable: Stable):
    st = await checksub(message.from_user.id)

    if st == 0:
        return

    sticker_file = FSInputFile(config["StickerMJ"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)
    await state.set_state(ClientState.process)

    config_dict = {}
    track_id = generate_random_text()
    matches = re.findall(r'-(\w+)\s+([\w\s:]+)(?=\s*-|\s*$)', message.text)
    request: str = re.sub(r'-\w+\s+[\w\s:]+(?=\s*-|\s*$)', '', message.text)
    wh_data = stable.ratio.split(':')
    width = int(wh_data[0])
    height = int(wh_data[1])

    for match in matches:
        config_name, config_value = match
        config_dict[config_name] = config_value

    request_dict = {
        "version": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "webhook": config['WebHookUrl'] + "/replicate/stable",
        "input": {
            "user_id": message.from_user.id,
            "wait_msg_id": wait_msg.message_id,
            "width": width,
            "height": height,
            "prompt": request,
            "negative_prompt": config_dict.get("neg", config['NegativeDefault']),

            "disable_safety_checker": True,
            "guidance_scale": int(config_dict.get("scale", 7)),
            "num_inference_steps": int(config_dict.get("steps", 50))
        }
    }

    try:
        await replicate(request_dict)
    except Exception as e:
        lg.error(e)
        await state.update_data(
            mj_status="error"
        )
        await state.set_state()
        await wait_msg.delete()
        return await message.answer(
            text=get_text("text.error_gpt")
        )

    await state.update_data(
        wait_msg_id=wait_msg.message_id,
        mj_status=f"process_{track_id}",
        action="prompt"
    )

    asyncio.create_task(
        check_mj_status(
            chat_id=message.from_user.id,
            track_id=track_id,
            request=request,
            wait_msg_id=wait_msg.message_id,
            state=state
        )
    )


async def stable_upscale(call: CallbackQuery, state: FSMContext, user: Clients):
    await state.set_state(ClientState.process)
    sticker_file = FSInputFile(config["StickerMJ"])
    wait_msg = await call.message.answer_sticker(
        sticker=sticker_file
    )

    await call.message.edit_reply_markup(
        reply_markup=kb.read_keyboard(
            keyboard=call.message.reply_markup,
            action=call.data
        )
    )

    photo = call.message.photo[-1].file_id
    track_id = generate_random_text()
    photofile = await bot.get_file(photo)
    path = photofile.file_path

    photo_url = f"https://api.telegram.org/file/bot{config['BotToken']}/{path}"

    request_dict = {
        "version": "42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
        "webhook": config['WebHookUrl'] + "/replicate/deepai",
        "input": {
            "user_id": call.from_user.id,
            "wait_msg_id": wait_msg.message_id,
            "track_id": track_id,

            "image": photo_url
        }
    }

    try:
        await replicate(request_dict)
    except Exception as e:
        await state.set_state()
        await state.update_data(
            mj_status="error"
        )
        await wait_msg.delete()
        await call.message.answer(get_text("text.error_gpt"))
        return lg.error(f"ERROR STABLE UPSCALE - {e}")

    await state.set_state(ClientState.process)
    await state.update_data(
        mj_status=track_id,
        action="upscale"
    )

    asyncio.create_task(
        check_mj_status(
            chat_id=call.from_user.id,
            track_id=track_id,
            request=f"увеличение фото {photo_url}",
            wait_msg_id=wait_msg.message_id,
            state=state
        )
    )


async def stable_retry(call: CallbackQuery, state: FSMContext, stable: Stable, session: Session):
    await call.answer()

    pic_code = call.data.split('_')[1]
    prompt = await session.scalar(
        select(Temp.prompt)
        .where(Temp.pic_code == pic_code)
    )

    await call.message.edit_reply_markup(
        reply_markup=kb.read_keyboard(
            keyboard=call.message.reply_markup,
            action=call.data
        )
    )

    sticker_file = FSInputFile(config["StickerMJ"])
    wait_msg = await call.message.answer_sticker(sticker=sticker_file)
    track_id = generate_random_text()
    await state.set_state(ClientState.process)

    config_dict = {}
    track_id = generate_random_text()
    matches = re.findall(r'-(\w+)\s+([\w\s:]+)(?=\s*-|\s*$)', prompt)
    request: str = re.sub(r'-\w+\s+[\w\s:]+(?=\s*-|\s*$)', '', prompt)
    wh_data = stable.ratio.split(':')
    width = int(wh_data[0])
    height = int(wh_data[1])

    for match in matches:
        config_name, config_value = match
        config_dict[config_name] = config_value

    request_dict = {
        "version": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "webhook": config['WebHookUrl'] + "/replicate/stable",
        "input": {
            "user_id": call.from_user.id,
            "wait_msg_id": wait_msg.message_id,
            "width": width,
            "height": height,
            "prompt": request,
            "negative_prompt": config_dict.get("neg", config['NegativeDefault']),

            "disable_safety_checker": True,
            "guidance_scale": int(config_dict.get("scale", 7)),
            "num_inference_steps": int(config_dict.get("steps", 50))
        }
    }

    try:
        await replicate(request_dict)
    except Exception as e:
        lg.error(e)
        await state.update_data(
            mj_status="error"
        )
        await state.set_state()
        await wait_msg.delete()
        return await call.message.answer(
            text=get_text("text.error_gpt")
        )

    await state.update_data(
        wait_msg_id=wait_msg.message_id,
        mj_status=f"process_{track_id}",
        action="prompt"
    )

    asyncio.create_task(
        check_mj_status(
            chat_id=call.from_user.id,
            track_id=track_id,
            request=request,
            wait_msg_id=wait_msg.message_id,
            state=state
        )
    )
