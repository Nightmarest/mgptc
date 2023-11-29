import openai
from aiogram.types import Message, FSInputFile
from utils.func import check_ban_words
from config_data.config import config
from config_data.create_bot import bot, db
from utils.func import get_text


openai.api_key = config['APIToken']


async def dalle_image(message: Message):
    prompt = message.text
    chat_id = message.from_user.id
    sticker_file = FSInputFile(config["StickerGPT"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)
    wait_msg_id = wait_msg.message_id

    ban_word = check_ban_words(prompt)
    if ban_word:
        await wait_msg.delete()
        return await message.answer(f"{get_text('text.ban_words')} - <code>{ban_word}</code>")

    response = await openai.Image.acreate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="standard",
        response_format="url",
    )

    await bot.delete_message(
        chat_id=chat_id,
        message_id=wait_msg_id
    )
    photo = response['data'][0]['url']
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=get_text("text.dalle_after_progress"), parse_mode='html')
    reqs = db.read(chat_id, "requests_dalle") - 1
    db.update(chat_id, "requests_dalle", reqs) if reqs >= 0 else ...
