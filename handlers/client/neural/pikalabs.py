import asyncio
import logging as lg

from aiogram.types import FSInputFile, Message
from aiogram.fsm.context import FSMContext

from config_data.create_bot import bot, db
from config_data.config import config
from services.neural.pikalabs import prompt_to_video
from filters.states.state import ClientState
from config_data.config import config
from config_data.config_load import discord_relax_cycle
from utils.func import (
    get_text, clean, generate_random_text, check_ban_words, check_mj_status, checksub
)


async def pikalabs_prompt(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    st = await checksub(chat_id)
    if st != 0:
        for char in message.text:
            if ord(char) in range(ord('а'), ord('я')+1):
                return await message.answer("⚠️ Обнаружена кириллица! Пожалуйста, используйте английский язык для запросов.")

        try:

            request = clean(message.text.lower())[:2056]
            ban_word = check_ban_words(request)
            if ban_word:
                await message.answer(f"{get_text('text.ban_words')} - <code>{ban_word}</code>")
                return

            await state.set_state(ClientState.process)
            sticker_file = FSInputFile(config["StickerMJ"])
            wait_msg = await message.answer_sticker(sticker=sticker_file)
            wait_msg_id = wait_msg.message_id
            track_id = generate_random_text()

            await state.update_data(
                wait_msg_id = wait_msg.message_id,
                mj_status=f"progress_{track_id}"
            )

            discord_config = next(discord_relax_cycle)
            await prompt_to_video(request, discord_config)

            db.delete_record(chat_id)
            db.stack_record(chat_id, request)

            await state.update_data(
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
            await state.set_state()
            await message.answer(get_text('text.mj_error'))
            lg.error(f"ZEROSCOPE PROMPT {e}")
            await bot.delete_message(
                chat_id=chat_id,
                message_id=wait_msg_id
            )