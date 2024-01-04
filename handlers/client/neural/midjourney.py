import asyncio
import logging as lg
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from filters.states.state import ClientState
from utils.json import read_json
from utils.func import (
    get_text, generate_random_text,
    check_mj_status, check_ban_words, clean,
    check_photo_nsfw, shorten_url, checksub
)

from config_data.create_bot import bot, db
from config_data.config_load import discord_relax_cycle, discord_fast_cycle
from keyboards.client_kb import kb
from config_data.config import config
from services.neural.mj import midjourney


async def midjourney_prompt(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    st = await checksub(chat_id)
    if st != 0:
        try:
            sticker_file = FSInputFile(config["StickerMJ"])
            wait_msg = await message.answer_sticker(sticker=sticker_file)


            if message.photo and message.caption:
                file = await bot.get_file(message.photo[-1].file_id)
                photo_url = f"https://api.telegram.org/file/bot{config['BotToken']}/{file.file_path}"
                photo_url = await shorten_url(photo_url)
                record_request = clean(message.caption.lower())[:2056]

                if await check_photo_nsfw(photo_url):
                    await wait_msg.delete()
                    return await message.answer("⛔️ Картинка содержит запрещенные элементы.")
                else:
                    request = f"{photo_url} {clean(message.caption.lower())[:2056]}"
            else:
                data = await state.get_data()
                if "prompt_temp" in data:
                    prompt_temp: str = data["prompt_temp"]
                if await state.get_state() == ClientState.prompt_add:
                    request = clean(prompt_temp.format(message.text.lower()))[:2056]
                    record_request = clean(prompt_temp.format(message.text.lower()))[:2056]
                else:
                    record_request = clean(message.text.lower())[:2056]
                    request = clean(message.text.lower())[:2056]

            ban_word = check_ban_words(request)
            if ban_word:
                await wait_msg.delete()
                return await message.answer(f"{get_text('text.ban_words')} - <code>{ban_word}</code>")

            await state.set_state(ClientState.process)

            track_id = generate_random_text()
            premium_type = db.read(chat_id, "premium_type")
            requests_mj = db.read(chat_id, 'requests_mj')
            requested = db.read(chat_id, "requested")
            db.update(chat_id, "requested", int(requested) + 1)
            discord_config = next(discord_fast_cycle) if (premium_type and requests_mj > 0) else next(discord_relax_cycle)
            response = await midjourney.prompt(request, discord_config)

            if response != 204:
                raise Exception(
                    f"ERROR RESPONSE <code>{response}</code>\nCHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>"
                )

            db.delete_record(chat_id)
            db.stack_record(chat_id, record_request)

            await state.update_data(
                action_type="text_generation",
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
            await state.set_state()
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
        request_data = db.read_temp(message_code)
        track_id = generate_random_text()
        for key, value in discord_list.items():
            for account in value:
                if account["name"] == request_data.discord_name:
                    discord_config = account
                    break
        sticker_file = FSInputFile(config["StickerMJ"])
        wait_msg = await call.message.answer_sticker(sticker=sticker_file)

        # UPSCALE
        if action_type in ["mj_u1", "mj_u2", "mj_u3", "mj_u4"]:
            await state.set_state(ClientState.process)

            await call.message.edit_reply_markup(
                reply_markup=kb.read_keyboard(
                    call.message.reply_markup,
                    call.data
                )
            )
            response = await midjourney.upscale(
                config["mj_u_scales"][action_type],
                request_data.target_id, request_data.target_hash,
                discord_config
            )

        # VARIATION
        elif action_type in ["mj_v1", "mj_v2", "mj_v3", "mj_v4"]:
            await state.set_state(ClientState.process)

            await call.message.edit_reply_markup(
                reply_markup=kb.read_keyboard(
                    call.message.reply_markup,
                    call.data
                )
            )
            response = await midjourney.variation(
                config["mj_v_scales"][action_type],
                request_data.target_id, request_data.target_hash,
                discord_config
            )

        # ZOOM
        elif action_type in ["mj_zoom1", "mj_zoom2"]:
            await state.set_state(ClientState.process)

            await call.message.edit_reply_markup(
                reply_markup=kb.read_keyboard(
                    call.message.reply_markup,
                    call.data
                )
            )
            response = await midjourney.zoom(
                config["mj_zoom"][action_type],
                request_data.target_id, request_data.target_hash,
                discord_config
            )

        if response != 204:
            raise Exception(
                f"ERROR RESPONSE <code>{response}</code>\nCHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>"
            )

        db.delete_record(chat_id)
        db.stack_record(chat_id, request_data.prompt)

        await state.update_data(
            discord_config = discord_config,
            action_type = action_type,
            wait_msg_id = wait_msg.message_id,
            mj_status=f"progress_{track_id}"
        )
        asyncio.create_task(
            check_mj_status(
                chat_id, track_id, request_data.prompt,
                wait_msg.message_id, state
            )
        )
    except Exception as e:
        lg.error(f"{e} from id: {chat_id}")
        await state.set_state()
        await call.message.answer(get_text("text.mj_error"))
        await bot.delete_message(
            chat_id=chat_id,
            message_id=wait_msg.message_id
        )