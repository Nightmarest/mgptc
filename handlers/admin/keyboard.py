from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram_widgets.pagination import KeyboardPaginator
from config_data.config import config
from config_data.create_bot import router_admin
from utils.json import read_json
from config_data.config_load import pay_list


class kb:
    def admin_menu():
        b1 = InlineKeyboardButton(
            text = '📩 Рассылка',
            callback_data= 'adm_mail'
        )
        b2 = InlineKeyboardButton(
            text = '👥 ОП',
            callback_data= 'adm_sub'
        )
        b3 = InlineKeyboardButton(
            text = '📊 Cтатистика',
            callback_data= 'adm_stat'
        )
        b4 = InlineKeyboardButton(
            text = '⛓ Ссылки',
            callback_data= 'adm_link'
        )
        b5 = InlineKeyboardButton(
            text = '📃 Скачать БД',
            callback_data= 'adm_bd'
        )
        b6 = InlineKeyboardButton(
            text = '♿️ Удалить неактивных',
            callback_data= 'adm_dead'
        )
        b7 = InlineKeyboardButton(
            text = '🔁 Рестарт',
            callback_data= 'adm_restart'
        )
        b8 = InlineKeyboardButton(
            text='✏️ Редактировать текст',
            callback_data='adm_text'
        )
        b9 = InlineKeyboardButton(
            text='💰 Подписки',
            callback_data="subpanel"
        )
        b10 = InlineKeyboardButton(
            text='🔑 Добавить промокод',
            callback_data="promo"
        )
        b11 = InlineKeyboardButton(
            text='⏱️ Выдача подписок',
            callback_data="recsub"
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1, b2],
                                                     [b3, b4],
                                                     [b5, b7],
                                                     [b8, b9],
                                                       [b10, b11],
                                                        [b6]])

    def go_back(section = 'menu'):
        b1 = InlineKeyboardButton(
            text = '⬅️ Назад',
            callback_data= f'adm_{section}'
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1]])


    def sub():
        b1 = InlineKeyboardButton(
            text = '🆕 Добавить',
            callback_data= 'sub_add'
        )
        b2 = InlineKeyboardButton(
            text = '🚮 Удалить',
            callback_data= 'sub_delete'
        )
        b3 = InlineKeyboardButton(
            text = '⬅️ Назад',
            callback_data= 'adm_menu'
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1, b2],
                                                       [b3]])


    def link(db_ref: list) -> InlineKeyboardMarkup:
        additional_buttons = [
            [
                InlineKeyboardButton(
                    text = '🆕 Добавить',
                    callback_data= 'link_add'
                ),
                InlineKeyboardButton(
                    text = '⬅️ Назад',
                    callback_data= 'adm_menu'
                )
            ]
        ]

        ref_button_list = []
        i = 0
        for ref_element in db_ref:
            name = ref_element[0]
            count = ref_element[1]
            token = ref_element[2]
            i += 1

            ref_button_list.append(
                InlineKeyboardButton(
                    text=f"{i}) {name} - {count} 👥",
                    callback_data=f"linkstat_{token}"
                )
            )

        return KeyboardPaginator(
            data=ref_button_list,
            additional_buttons=additional_buttons,
            router=router_admin,
        ).as_markup()


    def link_manage(token: str) -> InlineKeyboardMarkup:
        keyboard_list = []
        keyboard_list.append([
            InlineKeyboardButton(
                text="🚮 Удалить",
                callback_data=f"linkdelete_{token}"
            ),
            InlineKeyboardButton(
                text = '⬅️ Назад',
                callback_data= 'adm_link'
            )
        ])

        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def mailling():
        b1 = InlineKeyboardButton(
            text = '🚫 Стоп-кран',
            callback_data= 'mail_stop'
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1]])


    def end_mailling():
        b1 = InlineKeyboardButton(
            text = '♿️ Удалить неактивных',
            callback_data= 'adm_dead'
        )
        b2 = InlineKeyboardButton(
            text = '⬅️ Назад',
            callback_data= 'adm_menu'
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1],
                                                     [b2]])


    def sub_choise():
        b1 = InlineKeyboardButton(
            text = '👥 Канал',
            callback_data= 'sub_channel'
        )
        b2 = InlineKeyboardButton(
            text = '🤖 Бот',
            callback_data= 'sub_bot'
        )
        b3 = InlineKeyboardButton(
            text = '👥 Канал БП',
            callback_data= 'sub_skip-channel'
        )
        b4 = InlineKeyboardButton(
            text = '🤖 Бот БП',
            callback_data= 'sub_skip-bot'
        )
        b5 = InlineKeyboardButton(
            text = '⬅️ Назад',
            callback_data= 'adm_sub'
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1, b2],
                                                    [b3, b4],
                                                    [b5]])


    def text():
        langs = read_json(config["LangsAdmin"])
        text: dict = langs['text']
        buttons = []
        for key, value in text.items():
            buttons.append(
                InlineKeyboardButton(
                    text=value,
                    callback_data=f"text:{key}"
                )
            )
        back = [[InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data='adm_menu'
        )]]
        return KeyboardPaginator(
            data=buttons,
            additional_buttons=back,
            router=router_admin,
        ).as_markup()


    def text_call_handler(section):
        b1 = InlineKeyboardButton(
            text='✏️ Изменить',
            callback_data=f'update_text:{section}'
        )
        b2 = InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data='adm_text'
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1],
                                                     [b2]])

    def subadmin(id):
        b2 = InlineKeyboardButton(
            text='Добавить запросов',
            callback_data = f"req:plus:{id}"
        )
        b3 = InlineKeyboardButton(
            text='Убавить запросов',
            callback_data=f"req:minus:{id}"

        )
        b4 = InlineKeyboardButton(
            text="✅ Подключить подписку",
            callback_data=f"subattach:{id}"

        )
        b5 = InlineKeyboardButton(
            text="❌ Удалить подписку",
            callback_data=f"subdel:{id}"

        )

        return InlineKeyboardMarkup(inline_keyboard=[[b4],
                                                     [b2, b3],
                                                     [b5]])

    def choose_ai(type):
        b1 = InlineKeyboardButton(
            text='🌙 ChatGPT',
            callback_data=f"ai:{type}:gpt"
        )
        b2 = InlineKeyboardButton(
            text='🍬 SD+GPT',
            callback_data = f"ai:{type}:mj"
        )
        b3 = InlineKeyboardButton(
            text='🍬 PikaLabs',
            callback_data=f"ai:{type}:pika"
        )
        b4 = InlineKeyboardButton(
            text="🌇 DeepAI",
            callback_data=f"ai:{type}:deepai"
        )
        b5 = InlineKeyboardButton(
            text="🎈 Dall-E",
            callback_data=f"ai:{type}:dalle"
        )

        return InlineKeyboardMarkup(inline_keyboard=[[b1], [b2],
                                                     [b3], [b4],
                                                        [b5]])




    def time_choose():
        b1 = InlineKeyboardButton(
            text='День',
            callback_data=f"givesub:day"
        )
        b2 = InlineKeyboardButton(
            text='Неделя',
            callback_data = f"givesub:week"
        )
        b3 = InlineKeyboardButton(
            text='Месяц',
            callback_data=f"givesub:month"
        )
        b4 = InlineKeyboardButton(
            text="Год",
            callback_data=f"givesub:year"
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1], [b2],
                                                     [b3], [b4]])


    def choose_mode(data):
        b1 = InlineKeyboardButton(
            text='✅ Всем подписчикам нейросети',
            callback_data=f"recursive:all:{data}"
        )
        b2 = InlineKeyboardButton(
            text='⚠️ Опреленным тарифам',
            callback_data=f"givesub:manual:{data}"
        )
        return InlineKeyboardMarkup(inline_keyboard=[[b1], [b2]])
