import openai
from openai.error import InvalidRequestError
import logging as lg

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from filters.states.state import ClientState
from utils.func import check_ban_words
from config_data.config import config
from config_data.create_bot import bot, db
from utils.func import get_text


openai.api_key = config['APIToken']


async def dalle_image(message: Message, state: FSMContext):
    prompt = message.text
    chat_id = message.from_user.id
    sticker_file = FSInputFile(config["StickerGPT"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)

    ban_word = check_ban_words(prompt)
    if ban_word:
        await wait_msg.delete()
        return await message.answer(get_text("text.error_gpt"))

    await state.set_state(ClientState.process)

    try:
        response = await openai.Image.acreate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            response_format="url",
        )
    except Exception as e:
        await wait_msg.delete()
        await state.set_state()
        await message.answer(get_text("text.error_gpt"))
        return lg.error(f"ERROR DALLE - {e}")

    await state.set_state()
    await wait_msg.delete()

    photo = response['data'][0]['url']
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=get_text("text.dalle_after_progress"), parse_mode='html')
    reqs = db.read(chat_id, "requests_dalle") - 1
    db.update(chat_id, "requests_dalle", reqs) if reqs >= 0 else ...
