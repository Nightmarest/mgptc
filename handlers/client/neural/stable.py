import asyncio
import aiohttp
import io
import requests
import random

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, BufferedInputFile
from sqlalchemy.orm import Session
from sqlalchemy import select

from filters.states.state import ClientState
from database.models import Stable, Clients, Temp
from config_data.create_bot import config, bot
from keyboards.client_kb import kb

from services.neural.stable import stable_pic
from services.neural.deepai import upscale_photo
from utils.func import check_mj_status, generate_random_text, get_text, clean



async def stable_prompt(message: Message, state: FSMContext, stable: Stable):
    for char in message.text:
        if ord(char) in range(ord('а'), ord('я')+1):
            return await message.answer("⚠️ Обнаружена кириллица! Пожалуйста, используйте английский язык для запросов.")


    sticker_file = FSInputFile(config["StickerMJ"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)

    if await state.get_state() == ClientState.prompt_add:
        data = await state.get_data()
        if "prompt_temp" in data:
            prompt_temp: str = data["prompt_temp"]
        request = clean(prompt_temp.format(message.text.lower()))[:2056]
    else:
        request = clean(message.text.lower())[:2056]

    track_id = generate_random_text()
    await state.set_state(ClientState.process)

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

    response = await stable_pic(
        prompt=request,
        ratio=stable.ratio,
        model=stable.model,
        track_id=f"{message.from_user.id}_{track_id}_{request}"
    )

    if not response:
        await state.update_data(
            mj_status="error"
        )
        await state.set_state()
        await wait_msg.delete()
        await message.answer(get_text("text.error_gpt"))


async def stable_upscale(call: CallbackQuery, state: FSMContext, user: Clients):
    await state.set_state(ClientState.process)
    sticker_file = FSInputFile(config["StickerMJ"])
    wait_msg = await call.message.answer_sticker(sticker=sticker_file)

    await call.message.edit_reply_markup(
        reply_markup=kb.read_keyboard(
            keyboard=call.message.reply_markup,
            action=call.data
        )
    )

    photo = call.message.photo[-1].file_id
    chat_id = call.from_user.id

    photofile = await bot.get_file(photo)
    path = photofile.file_path

    photo_url = f"https://api.telegram.org/file/bot{config['BotToken']}/{path}"
    output = await upscale_photo(photo_url)
    img_data = requests.get(output).content

    await bot.delete_message(
        chat_id=chat_id,
        message_id=wait_msg.message_id
    )

    await state.set_state()

    image = BufferedInputFile(
        file=io.BytesIO(img_data).getvalue(),
        filename=f"{call.from_user.id}_{generate_random_text()}.jpg"
    )

    await bot.send_document(
        chat_id=call.from_user.id,
        document=image,
        caption=get_text("text.mj_after_progress_upscale"),
        reply_markup=kb.stable_menu()
    )

    user.requests_mj_today += 1
    if user.requests_mj > 0:
        user.requests_mj -= 1


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

    await state.update_data(
        wait_msg_id=wait_msg.message_id,
        mj_status=f"process_{track_id}",
        action="prompt"
    )

    asyncio.create_task(
        check_mj_status(
            chat_id=call.from_user.id,
            track_id=track_id,
            request=prompt,
            wait_msg_id=wait_msg.message_id,
            state=state
        )
    )

    response = await stable_pic(
        prompt=prompt,
        ratio=stable.ratio,
        model=stable.model,
        track_id=f"{call.from_user.id}_{track_id}_{prompt}"
    )

    if not response:
        await state.update_data(
            mj_status="error"
        )
        await state.set_state()
        await call.message.answer(
            text=get_text("text.error_gpt")
        )
