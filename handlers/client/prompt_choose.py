from aiogram.types import (Message, InlineQuery,
                           InlineQueryResultArticle, InputTextMessageContent
)
from aiogram.fsm.context import FSMContext

from database.models import Clients
from utils.func import get_text
from utils.json import read_json
from filters.states.state import ClientState
from config_data.config import config


async def prompt_choose(query: InlineQuery, user: Clients):
    if user.id is None:
        return

    data: dict = read_json(config["PromptChoose"])
    result: list = []
    i = 0
    for value in data:
        i += 1
        result.append(InlineQueryResultArticle(
            id= str(i),
            title= value["title"],
            thumbnail_url= value["photo_url"],
            description = value["prompt"].replace('{}', '[объект]'),
            input_message_content=InputTextMessageContent(
                message_text= value["prompt"]
        )))
    await query.answer(result, is_personal=True, cache_time=20)


async def prompt_add(message: Message, state: FSMContext):
    await state.set_state(ClientState.prompt_add)
    await state.update_data(prompt_temp = message.text)
    await message.delete()
    await message.answer(f"{get_text('text.prompt_add')}\n\n<code>{message.text.replace('{}', '[объект]')}</code>")