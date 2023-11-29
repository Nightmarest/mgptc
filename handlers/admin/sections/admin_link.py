from aiogram.types import Message, FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from handlers.admin.keyboard import kb
from handlers.admin.state import AdminState

from utils.func import generate_random_text
from handlers.admin.process import func
from config_data.create_bot import db
from config_data.config import config


async def link_add_one(call: CallbackQuery, state: FSMContext):
    step = call.data.split('_')[1]

    await state.set_state(AdminState.link_add)
    await call.message.edit_text("<b>⛓ Отправь название ссылки.</b>",
                                    reply_markup=kb.go_back("link"))


async def link_add_two(message: Message, state: FSMContext):
    try:
        link_token = generate_random_text()
        db.add_ads(message.text, link_token)

        await message.answer(f"<b>✅ Реферальная ссылка <code>{message.text}</code> добавлена:\n\n</b>"
                             f"<code>https://t.me/{config['BotNickName']}?start=ads{link_token}</code>",
                            reply_markup=kb.go_back("link"))
    except Exception as e:
        await message.answer(f"Бот не может выполнить данный скрипт по причине: <code>{e}</code>",
                            reply_markup=kb.go_back("link"))
    finally:
        await state.set_state()


async def link_stats(call: CallbackQuery):
    token = call.data.split("_")[1]
    print(token)

    db_ads = db.admin_request(f"SELECT * FROM ads WHERE token = '{token}'")
    db_info = db.admin_request(f"SELECT join_date, buyer, dead FROM clients WHERE where_from='{token}'")
    db_date = db.admin_request(f"SELECT join_date FROM clients WHERE where_from='{token}'")
    stats_text = func.get_statslink_str(db_info, db_ads[0][0], db_ads[0][1])

    await call.message.delete()
    stats_msg = await call.message.answer_video(
        video="https://i.pinimg.com/originals/f0/f8/51/f0f8518804b731b18740d4f186fa42c6.gif",
        caption=stats_text,
        parse_mode="HTML",
        reply_markup= kb.link_manage(token)
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


async def link_delete(call: CallbackQuery, state: FSMContext):
    token_remove = call.data.split("_")[1]

    try:
        db.delete_ads(token_remove)

        await call.message.delete()
        await call.message.answer(
            text=f"<b>✅ Реф код [<code>{token_remove}</code>] удалён!</b>",
            reply_markup=kb.go_back("link")
        )
    except Exception as e:
        await call.message.answer(
            text=f"Бот не может выполнить данный скрипт по причине: <code>{e}</code>",
            reply_markup=kb.go_back("link")
        )
    finally:
        await state.set_state()
