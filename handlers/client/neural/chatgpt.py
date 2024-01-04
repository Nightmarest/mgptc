import logging as lg
import os

from aiogram.types import FSInputFile, BufferedInputFile, Message
from aiogram.fsm.context import FSMContext

from config_data.create_bot import bot, db
from config_data.config import config
from utils.func import get_text, clean, checksub
from services.neural.gpt import get_response_gpt, voice_to_text, text_to_voice
from filters.states.state import ClientState
from config_data.config import config


async def chatgpt_text(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    st = await checksub(chat_id)
    if st != 0:
        sticker_file = FSInputFile(config["StickerGPT"])
        wait_msg = await message.answer_sticker(sticker=sticker_file)
        wait_msg_id = wait_msg.message_id
        prompt = clean(message.text)

        try:
            await chatgpt_prompt(message, state, prompt, wait_msg_id)
        except Exception as e:
            lg.error(f"{e} from id: {chat_id}")
            await state.set_state()
            await message.answer(get_text("text.error_gpt"))
            await bot.delete_message(
                chat_id=chat_id,
                message_id=wait_msg_id
            )


async def chatgpt_voice(message: Message, state: FSMContext):
    chat_id = message.from_user.id

    if message.voice.duration > 60:
        return await message.answer("⛔️ <b>Ваше голосовое сообщение слишком длинное!</b>\n\n<i>Задайте пожалуйста его покороче.</i>")
    sticker_file = FSInputFile(config["StickerGPT"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)
    wait_msg_id = wait_msg.message_id
    voice_info = await bot.get_file(message.voice.file_id)
    voice_file = await bot.download_file(
        file_path=voice_info.file_path,
        destination=f"files/temp/voice_{chat_id}.ogg"
    )

    try:
        with open(f"files/temp/voice_{chat_id}.ogg", "rb") as voice_file:
            prompt = await voice_to_text(voice_file)
        os.remove(f"files/temp/voice_{chat_id}.ogg")
        await chatgpt_prompt(message, state, prompt, wait_msg_id)
    except Exception as e:
        lg.error(f"{e} from id: {chat_id}")
        await state.set_state()
        await message.answer(get_text("text.error_gpt"))
        await bot.delete_message(
            chat_id=chat_id,
            message_id=wait_msg_id
        )


async def chatgpt_prompt(message: Message, state: FSMContext, prompt: str, wait_msg_id: int):
    chat_id = message.from_user.id

    await state.set_state(ClientState.process)
    data = await state.get_data()
    print(data)
    dialog_list: list = data["dialog_list"]

    dialog_list, response = await get_response_gpt(dialog_list, prompt)
    await state.update_data(dialog_list= dialog_list)

    if db.read(chat_id, 'voice_answer'):
        voice = await text_to_voice(response)
        await message.answer_voice(
            voice=BufferedInputFile(
                voice.getvalue(),
                filename="audio.ogg"
            )
        )
    else:
        try:
            await message.answer(response, parse_mode='markdown')
        except Exception:
            await message.answer(response, parse_mode=None)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=wait_msg_id)
    except Exception:
        pass

    await state.set_state()
    # requested = db.read(chat_id, "requested")
    # db.update(chat_id, "requested", int(requested) + 1)
    reqs = db.read(chat_id, "requests_gpt") - 1
    db.update(chat_id, "requests_gpt", reqs) if reqs >= 0 else ...
