# AIOGRAM 3

import datetime
import sys, os


from aiogram.types import Message, FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from config_data.create_bot import db

from handlers.admin.keyboard import kb
from handlers.admin.state import AdminState
from handlers.admin.process import func
from config_data.config import config


async def admin_menu(message: Message):
    await message.answer('👑 Выберите пункт:',
                        reply_markup = kb.admin_menu())


async def admin_db(message: Message):
    try:
        finish = db.admin_request(message.text)
    except Exception as e:
        return await message.answer(str(e))
    else:
        await message.answer(f"Успешно <code>{str(finish)}</code>")


async def admin_call_handler(call: CallbackQuery, state: FSMContext):
    step = call.data.split("_")[1]

    # главное меню
    if step == 'menu':
        await state.set_state()

        await call.message.delete()
        await call.message.answer(
            text='<b>👑 Выберите пункт:</b>',
            reply_markup = kb.admin_menu()
        )


    # рассылка
    elif step == 'mail':
        await state.set_state(AdminState.mail)
        await call.message.edit_text("<b>📩 Перешлите рекламное сообщение.</b>"
                                     "\n\n<i>ℹ️ Рассылка начнётся сразу же после получения сообщения!</i>",
                                  reply_markup=kb.go_back())


    # ОП
    elif step == 'sub':
        await state.set_state()
        text = func.get_op()
        await call.message.edit_text("<b>👥 Меню ОП:</b>\n\n"
                                    f"{text}",
                                     reply_markup=kb.sub(),
                                     disable_web_page_preview=True)


    # Статистика
    elif step == 'stat':
        db_info = db.admin_request(f"SELECT join_date, buyer, where_from, dead FROM clients")
        db_date = db.admin_request("SELECT join_date FROM clients")
        stats_text = func.get_stats_str(db_info)

        await call.message.delete()
        stats_msg = await call.message.answer_video(
            video="https://i.pinimg.com/originals/f0/f8/51/f0f8518804b731b18740d4f186fa42c6.gif",
            caption=stats_text,
            parse_mode="HTML",
            reply_markup= kb.go_back()
        )

        img_bytes = func.get_stats_graph(db_date)

        await stats_msg.edit_media(
            media=InputMediaPhoto(
                media=BufferedInputFile(
                    img_bytes.getvalue(),
                    filename="stats.png",
                ),
                caption=stats_msg.html_text,
                parse_mode="HTML"
            ),
            reply_markup=stats_msg.reply_markup
        )


    elif step == 'link':
        await state.set_state()
        db_ref = db.admin_request(f"SELECT id, count, token FROM ads")

        await call.message.delete()
        await call.message.answer(
            text="<b>⛓ Реферальное меню:</b>",
            reply_markup=kb.link(db_ref))


    elif step == 'bd':
        wait_message = await call.message.edit_text("<b>📃 Подождите, идёт скачивание БД...</b>")

        try:
            with open("handlers/admin/user_ids.txt", "w") as file:
                user_id_list = db.admin_request(f"SELECT id FROM {config['BDTable']}")
                for user_id in user_id_list:
                    file.write(str(user_id[0]) + "\n")
            document = FSInputFile("handlers/admin/user_ids.txt")
            await call.message.answer_document(document= document,
                                               caption= f"<b>📃 Готово! БД {str(datetime.date.today())}</b>\n\n"
                                                         "Вернуться назад - /admin")
        except Exception as e:
            await call.message.answer(f"Бот не может выполнить данный скрипт по причине: <code>{e}</code>",
                                         reply_markup=kb.go_back())



    elif step == 'dead':
        wait_message = await call.message.edit_text("<b>♿️ Подождите, идёт удаление мёртвых пользователей...</b>")
        count_dead = len(db.admin_request(f"SELECT * FROM {config['BDTable']} WHERE dead = 1"))

        try:
            db.admin_request(f"DELETE FROM {config['BDTable']} WHERE dead = true")
            await wait_message.delete()
            await call.message.answer(f"<b>♿️ Успешно удалено {count_dead} мёртвых пользователей с БД!</b>",
                                         reply_markup=kb.go_back())
        except Exception as e:
            await call.message.answer(f"Бот не может выполнить данный скрипт по причине: <code>{e}</code>",
                                         reply_markup=kb.go_back())


    elif step == 'restart':
        await call.message.edit_text('<b>🔁 Перезапускаю...</b>\n\n'
                                     '<i>Ожидайте 5 секунд!</i>',
                                     reply_markup=kb.go_back())
        python = sys.executable
        os.execl(python, python, *sys.argv)


    elif step == 'text':
        await call.message.edit_text(
            text="<b>✏️ Поменять текст</b>\n\n"
                 "<i>Выберите по кнопке ниже нужный раздел.</i>",
            reply_markup=kb.text()
        )