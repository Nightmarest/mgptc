from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from handlers.admin.keyboard import kb
from handlers.admin.state import AdminState
from handlers.admin.process import func

from config_data.config import config
from utils.check_sub import add_channnel, remove_channel

async def sub_call_handler(call: CallbackQuery, state: FSMContext):
    if call.message.chat.id not in config["AdminList"]:
        return

    step = call.data.split("_")[1]

    if step == 'add':
        await call.message.edit_text("<b>👥 Выбери кого добавить:</b>\n\n"
                                     "<i>ℹ️ БП - без проверки.</i>",
                                     reply_markup=kb.sub_choise())

    elif step == 'delete':
        await state.set_state(AdminState.sub_delete)
        await call.message.edit_text("<b>👥 Ввведите ID канала/бота для его удаления.</b>",
                                    reply_markup=kb.go_back("sub"))

    elif step == 'channel':
        await state.update_data(skip = False)
        await state.set_state(AdminState.sub_add_channel_1)
        await call.message.edit_text("<b>👥 Перешли сообщение из тг канала.</b>",
                                    reply_markup=kb.go_back("sub"))

    elif step == 'bot':
        await state.update_data(skip = False)
        await state.set_state(AdminState.sub_add_bot_1)
        await call.message.edit_text("<b>👥 Отправьте токен бота.</b>",
                                    reply_markup=kb.go_back("sub"))

    elif step == 'skip-channel':
        await state.update_data(skip = True)
        await state.set_state(AdminState.sub_add_channel_1)
        await call.message.edit_text("<b>👥 Перешли сообщение из тг канала.</b>",
                                    reply_markup=kb.go_back("sub"))

    elif step == 'skip-bot':
        await state.update_data(skip = True)
        await state.set_state(AdminState.sub_add_bot_1)
        await call.message.edit_text("<b>👥 Отправьте токен бота.</b>",
                                    reply_markup=kb.go_back("sub"))


async def sub_delete(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
    except:
        await message.answer("<b>❌ Вы ввели не ID!</b>",
                            reply_markup=kb.go_back("sub"))
        return

    result = remove_channel(channel_id)

    if not result:
        await message.answer(f"<b>❌ Канал/Бот с ID <code>{message.text}</code> не найден!</b>",
                                    reply_markup=kb.go_back("sub"))
        return

    first_name, url, is_bot = result
    element = 'Бот' if is_bot else 'Канал'
    await message.answer(f"<b>✅ {element} <a href='{url}'>{first_name}</a> успешно удалён с ОП!</b>",
                                reply_markup=kb.go_back("sub"))
    await state.set_state()


async def sub_channel_forwarded(message: Message, state: FSMContext):
    try:
        channel_id = message.forward_from_chat.id
        first_name = message.forward_from_chat.title
    except Exception as e:
        await message.answer(f"<b>👥 Сообщение переслано не из канала❗️</b>\n\n<code>{str(e)}</code>",
                                    reply_markup=kb.go_back("sub"))
        return

    await state.update_data(channel_id= channel_id, first_name= first_name)
    await state.set_state(AdminState.sub_add_channel_2)

    await message.answer("<b>👥 Теперь отправьте ссылку приглашения в канал.</b>",
                                    reply_markup=kb.go_back("sub"))


async def sub_channel_url(message: Message, state: FSMContext):
    entities = message.entities
    url = ''

    for item in entities:
        if item.type == "url":
            url = message.text[item.offset:item.offset+item.length]

    if url == '':
        await message.answer("<b>👥 Вы не отправляли ссылку❗️</b>",
                                    reply_markup=kb.go_back("sub"))
        return

    data = await state.get_data()
    channel_id = data["channel_id"]
    first_name = data["first_name"]
    skip = data["skip"]

    try:
        add_channnel(channel_id=channel_id,
                     first_name=first_name,
                     url=url,
                     is_bot=False,
                     skip=skip)
    except Exception as e:
        await message.answer(f"❌ Бот не может выполнить данный скрипт по причине: <code>{e}</code>",
                            reply_markup=kb.go_back("sub"))
    else:
        skip_text = ' (БП) ' if skip else ' '
        await message.answer(f"<b>✅ Канал{skip_text}<code>{first_name}</code> успешно добавлен!</b>",
                                    reply_markup=kb.go_back("sub"))
    finally:
        await state.set_state()


async def sub_bot_token(message: Message, state: FSMContext):
    bot_info = await func.get_bot_info(message.text)

    if not bot_info:
        await message.answer(f"<b>❌ Токен бота недействителен!</b>",
                                    reply_markup=kb.go_back("sub"))
        return

    first_name = bot_info['first_name']
    username = bot_info['username']
    bot_id = bot_info['id']

    await state.update_data(first_name = bot_info['first_name'], bot_id=bot_id, token=message.text)
    await state.set_state(AdminState.sub_add_bot_2)

    await message.answer(f"<b>👥 Найден бот <a href='https://t.me/{username}'>{first_name}</a></b>\n\n"
                         "ℹ️ Теперь отправьте ссылку на бота.",
                                    reply_markup=kb.go_back("sub"),
                                    disable_web_page_preview=True)


async def sub_bot_url(message: Message, state: FSMContext):
    entities = message.entities
    url = ''

    for item in entities:
        if item.type == "url":
            url = message.text[item.offset:item.offset+item.length]

    if url == '':
        await message.answer("<b>👥 Вы не отправляли ссылку❗️</b>",
                                    reply_markup=kb.go_back("sub"))
        return

    bot_info = await state.get_data()

    first_name = bot_info['first_name']
    bot_id = bot_info['bot_id']
    token = bot_info['token']
    skip = bot_info["skip"]

    try:
        add_channnel(token=token,
                     first_name=first_name,
                     url=url,
                     is_bot=True,
                     channel_id=bot_id,
                     skip=skip)
    except Exception as e:
        await message.answer(f"❌ Бот не может выполнить данный скрипт по причине: <code>{e}</code>",
                            reply_markup=kb.go_back("sub"))
    else:
        skip_text = ' (БП) ' if skip else ' '
        await message.answer(f"<b>✅ Бот{skip_text}<code>{first_name}</code> успешно добавлен!</b>",
                                    reply_markup=kb.go_back("sub"))
    finally:
        await state.set_state()