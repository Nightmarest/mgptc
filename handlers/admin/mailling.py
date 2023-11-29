import asyncio
import logging as lg

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramRetryAfter

from config_data.create_bot import bot, db
from config_data.config import config
from handlers.admin.process import func
from handlers.admin.keyboard import kb

mailling_status = False
mailling_second = 0
dead_list = []
good_list = []


async def mailling_stop(call: CallbackQuery):
    global mailling_status
    if mailling_status:
        mailling_status = False
        await call.answer("Рассылка экстренно остановлена❗️")
    else:
        await call.answer("Рассылка в данный момент не работает❗️")


### ДАЛЬШЕ СКРИПТ РАССЫЛКИ


async def send_message(chat_id, message_id, reply_markup, from_chat_id):
    try:
        await bot.copy_message(chat_id=chat_id,
                               message_id=message_id,
                               from_chat_id= from_chat_id,
                               reply_markup=reply_markup)
    except TelegramRetryAfter as e:
        lg.error(f"ERROR SLEEP: {e}")
        await asyncio.sleep(e.retry_after)
        return await send_message(chat_id, message_id, reply_markup, from_chat_id)
    except Exception as e:
        return False
    else:
        return True


async def mailling_cycle(list_id, message_id, reply_markup, from_chat_id):
    global dead_list, good_list, mailling_status
    for chat_id, dead in list_id:
        if dead:
            dead_list.append(chat_id)
            continue
        elif not mailling_status:
            return
        result = await send_message(chat_id, message_id, reply_markup, from_chat_id)
        if not result:
            dead_list.append(chat_id)
        else:
            good_list.append(chat_id)


async def mailling_monitor(message: Message):
    global dead_list, good_list, mailling_status, mailling_second

    while mailling_status:
        try:
            await message.edit_text("<b>✉️ Идёт рассылка!</b>\n\n"
                                f"✅ Успешно отправлено: <code>{len(good_list)}</code>\n"
                                f"❌ Не отправлено: <code>{len(dead_list)}</code>\n"
                                f"🕘 Прошло секунд: <code>{mailling_second}</code>",
                                reply_markup=kb.mailling())
        except TelegramRetryAfter as e:
            lg.error(f"ERROR SLEEP MAILLING_MONITOR: {e}")
            mailling_second += e.retry_after
            await asyncio.sleep(e.retry_after)
        mailling_second += 5
        await asyncio.sleep(5)



async def mailling(message: Message, state: FSMContext):
    global dead_list, good_list, mailling_status, mailling_second

    await state.set_state()
    msg = await message.answer("<b>🔥 Рассылка начата!</b>")
    bd_list_id = db.admin_request(f"SELECT id, dead FROM {config['BDTable']}")
    divided_list_id = func.divide_list(bd_list_id, 20)
    tasks = []
    mailling_status = True

    asyncio.create_task(mailling_monitor(msg))

    for list_id in divided_list_id:
        task = asyncio.create_task(mailling_cycle(list_id, message.message_id, message.reply_markup, message.chat.id))
        tasks.append(task)

    await asyncio.gather(*tasks)

    try:
        # [1,2,3] -> 1,2,3
        tuple = ','.join(["{}".format(item) for item in dead_list])
        db.admin_request(f"UPDATE clients SET dead = true WHERE id IN ({tuple})")
    except Exception as e:
        await message.answer(f"Не смог обновить мёртвых в БД: <code>{e}</code>")

    await message.answer("<b>✉️ Рассылка завершена!</b>\n\n"
                        f"✅ Успешно отправлено: <code>{len(good_list)}</code>\n"
                        f"❌ Не отправлено: <code>{len(dead_list)}</code>\n"
                        f"🕘 Прошло секунд: <code>{mailling_second}</code>",
                        reply_markup=kb.end_mailling())

    mailling_status = False
    mailling_second = 0
    dead_list = []
    good_list = []