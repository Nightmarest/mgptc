import io
import logging as lg
import asyncio
import requests

from aiogram.types import FSInputFile, BufferedInputFile, Message
from aiogram.fsm.context import FSMContext

from config_data.config import config
from config_data.create_bot import bot, db
from services.neural.replicate import replicate
from utils.func import get_text, generate_random_text, checksub, check_mj_status
from filters.states.state import ClientState


async def deepai_image(message: Message, state: FSMContext):
    st = await checksub(message.from_user.id)
    if st != 0:
        sticker_file = FSInputFile(config["StickerGPT"])
        wait_msg = await message.answer_sticker(sticker=sticker_file)

        photo = message.photo[-1].file_id
        chat_id = message.from_user.id
        photofile = await bot.get_file(photo)
        path = photofile.file_path
        photo_url = f"https://api.telegram.org/file/bot{config['BotToken']}/{path}"
        track_id = generate_random_text()

        request_dict = {
            "version": "42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
            "webhook": config['WebHookUrl'] + "/replicate/deepai",
            "input": {
                "user_id": message.from_user.id,
                "wait_msg_id": wait_msg.message_id,
                "track_id": track_id,

                "image": photo_url
            }
        }

        try:
            await replicate(request_dict)
        except Exception as e:
            await wait_msg.delete()
            await state.set_state()
            await state.update_data(
                mj_status=""
            )
            await message.answer(get_text("text.error_gpt"))
            return lg.error(f"ERROR DEEPAI - {e}")

        await state.set_state(ClientState.process)
        await state.update_data(
            mj_status=track_id
        )

        asyncio.create_task(
            check_mj_status(
                chat_id=message.from_user.id,
                track_id=track_id,
                request=f"увеличение фото {photo_url}",
                wait_msg_id=wait_msg.message_id,
                state=state
            )
        )

        # img_data = requests.get(output).content

        # await bot.delete_message(
        #     chat_id=chat_id,
        #     message_id=wait_msg_id
        # )

        # image = BufferedInputFile(
        #     file=io.BytesIO(img_data).getvalue(),
        #     filename=f"{message.from_user.id}_{generate_random_text()}.jpg"
        # )

        # await bot.send_photo(chat_id=chat_id, caption=get_text("text.deepai_after_progress"), photo=image)
        # # requested = db.read(chat_id, "requested")
        # # db.update(chat_id, "requested", int(requested) + 1)
        # reqs = db.read(chat_id, "requests_deepai") - 1
        # db.update(chat_id, "requests_deepai", reqs) if reqs >= 0 else ...
