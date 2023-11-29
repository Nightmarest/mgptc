import io
import requests

from aiogram.types import FSInputFile, BufferedInputFile, Message
from aiogram.fsm.context import FSMContext

from config_data.config import config
from config_data.create_bot import bot, db
from services.neural.deepai import upscale_photo
from utils.func import get_text, generate_random_text


async def deepai_image(message: Message, state: FSMContext):
    sticker_file = FSInputFile(config["StickerGPT"])
    wait_msg = await message.answer_sticker(sticker=sticker_file)
    wait_msg_id = wait_msg.message_id

    photo = message.photo[-1].file_id
    chat_id = message.from_user.id
    photofile = await bot.get_file(photo)
    path = photofile.file_path
    photo_url = f"https://api.telegram.org/file/bot{config['BotToken']}/{path}"

    output = await upscale_photo(photo_url)
    img_data = requests.get(output).content

    await bot.delete_message(
        chat_id=chat_id,
        message_id=wait_msg_id
    )

    image = BufferedInputFile(
        file=io.BytesIO(img_data).getvalue(),
        filename=f"{message.from_user.id}_{generate_random_text()}.jpg"
    )

    await bot.send_photo(chat_id=chat_id, caption=get_text("text.deepai_after_progress"), photo=image)
    reqs = db.read(chat_id, "requests_deepai") - 1
    db.update(chat_id, "requests_deepai", reqs) if reqs >= 0 else ...
