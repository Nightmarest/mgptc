import asyncio
import logging as lg
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from filters.states.state import ClientState
from config_data.create_bot import bot, db, r
from config_data.config_load import discord_relax_cycle, discord_fast_cycle
from keyboards.client_kb import kb
from config_data.config import config
from services.neural.mj import midjourney
from utils.json import read_json
from utils.func import (
    get_text, generate_random_text,
    check_mj_status, check_ban_words, clean,
    check_photo_nsfw, shorten_url
)


async def midjourney_prompt(message: Message, state: FSMContext):
    chat_id = message.from_user.id

    try:
        if message.photo and message.caption:
            check_smile = await message.answer("🔎")
            check_msg = await message.answer("⏳ Подождите, идёт проверка картинки...")

            file = await bot.get_file(message.photo[-1].file_id)
            photo_url = f"https://api.telegram.org/file/bot{config['BotToken']}/{file.file_path}"
            photo_url = await shorten_url(photo_url)

            if await check_photo_nsfw(photo_url):
                await check_smile.delete()
                return await check_msg.edit_text("⛔️ Картинка содержит запрещенные элементы.")
            else:
                await check_smile.delete()
                await check_msg.delete()
                request = f"{photo_url} {clean(message.caption.lower())}"
        else:
            data = await state.get_data()
            if "prompt_temp" in data:
                prompt_temp: str = data["prompt_temp"]
            if await state.get_state() == ClientState.prompt_add:
                request = clean(prompt_temp.format(message.text))
            else:
                request = clean(message.text.lower())

        await state.set_state(ClientState.process_mj_prompt)

        ban_word = check_ban_words(request)
        if ban_word:
            await message.answer(f"{get_text('text.ban_words')} - <code>{ban_word}</code>")
            return

        track_id = generate_random_text()
        premium_type = db.read(chat_id, "premium_type")
        requests_mj = db.read(chat_id, 'requests_mj')
        discord_config = next(discord_fast_cycle) if (premium_type and requests_mj > 0) else next(discord_relax_cycle)

        sticker_file = FSInputFile(config["StickerMJ"])
        wait_msg = await message.answer_sticker(sticker=sticker_file)
        response = await midjourney.prompt(request, discord_config)

        if response != 204:
            raise Exception(
                f"ERROR RESPONSE <code>{response}</code>\nCHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>"
            )

        r.set(name=request,
              value=str(message.from_user.id),
              ex=config["MJTime"])
        await state.update_data(
            discord_config = discord_config,
            wait_msg_id = wait_msg.message_id,
            mj_status=f"progress_{track_id}"
        )
        asyncio.create_task(
            check_mj_status(
                chat_id, track_id, request,
                wait_msg.message_id, state
            )
        )

    except Exception as e:
        lg.error(f"{e} from id: {chat_id}")
        await state.set_state(ClientState.midjourney)
        await message.answer(get_text("text.mj_error"))
        await bot.delete_message(
            chat_id=chat_id,
            message_id=wait_msg.message_id
        )

async def midjourney_call(call: CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    discord_list = read_json(config["DiscordConfig"])
    data = call.data.split(":")

    if call.data == "mj_end":
        await call.answer("Вы уже генерировали данную картинку❗️")
        return

    try:
        message_code = data[1]
        action_type = data[0]
        request_data = r.hgetall(message_code)
        track_id = generate_random_text()
        for key, value in discord_list.items():
            for account in value:
                if account["name"] == request_data["discord_name"]:
                    discord_config = account
                    break
        sticker_file = FSInputFile(config["StickerMJ"])
        wait_msg = await call.message.answer_sticker(sticker=sticker_file)

        # UPSCALE
        if action_type in ["mj_u1", "mj_u2", "mj_u3", "mj_u4"]:
            await state.set_state(ClientState.process_mj_upscale)

            await call.message.edit_reply_markup(
                reply_markup=kb.read_keyboard(call.message.reply_markup, call.data)
            )
            response = await midjourney.upscale(
                config["mj_u_scales"][action_type],
                request_data['target_id'], request_data['target_hash'],
                discord_config
            )

        # VARIATION
        elif action_type in ["mj_v1", "mj_v2", "mj_v3", "mj_v4"]:
            await state.set_state(ClientState.process_mj_prompt)

            await call.message.edit_reply_markup(
                reply_markup=kb.read_keyboard(call.message.reply_markup, call.data)
            )
            response = await midjourney.variation(
                config["mj_v_scales"][action_type],
                request_data['target_id'], request_data['target_hash'],
                discord_config
            )

        # ZOOM
        elif action_type in ["mj_zoom1", "mj_zoom2"]:
            await state.set_state(ClientState.process_mj_prompt)

            await call.message.edit_reply_markup(
                reply_markup=kb.read_keyboard(call.message.reply_markup, call.data)
            )
            response = await midjourney.zoom(
                config["mj_zoom"][action_type],
                request_data['target_id'], request_data['target_hash'],
                discord_config
            )

        if response != 204:
            raise Exception(
                f"ERROR RESPONSE <code>{response}</code>\nCHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>"
            )

        r.set(name=request_data['prompt'],
              value=str(call.from_user.id),
              ex=config["MJTime"])
        await state.update_data(
            discord_config = discord_config,
            wait_msg_id = wait_msg.message_id,
            mj_status=f"progress_{track_id}"
        )
        asyncio.create_task(
            check_mj_status(
                chat_id, track_id, request_data['prompt'],
                wait_msg.message_id, state
            )
        )
    except Exception as e:
        lg.error(f"{e} from id: {chat_id}")
        await state.set_state(ClientState.midjourney)
        await call.message.answer(get_text("text.mj_error"))
        await bot.delete_message(
            chat_id=chat_id,
            message_id=wait_msg.message_id
        )