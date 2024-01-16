from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from config_data.config import MODELS_STABLE
from config_data.config import config
from config_data.config_load import pay_list
from utils.func import get_text


class kb:
    # Start Keyboard
    def start_agreement():
        b1 = KeyboardButton(text = get_text("buts.agreement_ok"))
        kb_agreement = ReplyKeyboardMarkup(
            row_width=1, resize_keyboard=True,
            one_time_keyboard = True, keyboard = [[b1]]
        )

        return kb_agreement
    def start():
        b1 = KeyboardButton(text = get_text("buts.choise_mode"))
        b2 = KeyboardButton(text = get_text("buts.help"))
        b3 = KeyboardButton(text = get_text("buts.profile"))
        # b4 = KeyboardButton(text = get_text("buts.premium"))
        b4 = KeyboardButton(text = get_text("buts.restart"))

        kb_start = ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True, one_time_keyboard=False,
            keyboard=[[b1, b3],
                      [b2, b4]

            ]
        )
        return kb_start


    def panel_mode():
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text = get_text('buts.change_mode'),
            callback_data= 'change_mode'
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def profile(premium_type: str, course: bool, voice_answer: bool, auto: bool, autov2: bool):
        if premium_type:
            query_menu = pay_list[premium_type]["menu_prompt"]
        else:
            query_menu = False
        if voice_answer:
            voice_text = "⚙️ Голосовые ответы от ChatGPT: вкл."
        else:
            voice_text = "⚙️ Голосовые ответы от ChatGPT: выкл."
        keyboard_list = []

        if course:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text('buts.profile_education'),
                url= config["EducationUrl"]
            )])
        else:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text('buts.profile_education'),
                callback_data= "description_buy-3_buy-3"
            )])

        keyboard_list.append([InlineKeyboardButton(
            text = get_text('buts.profile_forum'),
            url = config["ForumUrl"]
        )])

        keyboard_list.append([InlineKeyboardButton(
            text=voice_text,
            callback_data="switch_voice_answer"
        )])

        if auto is True:
            keyboard_list.append([InlineKeyboardButton(
                text=get_text("buts.autoup"),
                callback_data="disable_autoup"
            )])
        # keyboard_list.append([InlineKeyboardButton(
        #     text="Отключить предыдущие подписки",
        #     callback_data="disable_autoup_recursive"
        # )])

        if autov2 is True:
            keyboard_list.append([InlineKeyboardButton(
                # text=get_text("buts.autoup"),
                text="Управление подписками",
                callback_data="disable_autoups"
            )])


        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def change_mode():
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text = 'ChatGPT 4',
            callback_data='chatgpt_mode'
        )])
        keyboard_list.append([InlineKeyboardButton(
            text = "Stable Diffusion XL",
            callback_data="stable_mode"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text = "Pika Labs",
            callback_data="pikalabs_mode"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text = "DALLE",
            callback_data="dalle_mode"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text = "DeepAI",
            callback_data="deepai_mode"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def back_to_profile():
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text = "⬅️ Вернуться назад",
            callback_data= "call_profile"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def pay_list_keyboard(type: str, auto: bool):
        keyboard_list = []
        for key, value in pay_list.items():
            if value["type"] != type:
                continue
            if value["skip_buy_handler"]:
                continue
            text = value["callback_text"]
            callback_data = f"description_{key}_{type}"
            keyboard_list.append([InlineKeyboardButton(
                text=text,
                callback_data=callback_data)])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.back"),
            callback_data="back_to_premium"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)

    def promostage():
        keyboard_list = []

        keyboard_list.append([InlineKeyboardButton(
            text="Без промокода",
            callback_data="back_to_premium"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    # Покупка запросов
    def premium():
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text="ChatGPT",
            callback_data="choose_premium:gpt"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text="Midjourney + ChatGPT",
            callback_data="choose_premium:mj+gpt"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text="Pika Labs",
            callback_data="choose_premium:zeroscope"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text="DeepAI",
            callback_data="choose_premium:deepai"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def description_premium(data: str, type: str):
        buy_type = data.replace("(skip)", "")
        keyboard_list = []

        if buy_type == "buy-3":
            buy_text = get_text("buts.premium_buy_course")
        else:
            buy_text = get_text("buts.premium_buy")
        keyboard_list.append([InlineKeyboardButton(
            text=buy_text,
            callback_data=buy_type
        )])

        if (pay_list[buy_type]["course"]) and not (pay_list[buy_type]["skip_buy_handler"]) and not ("(skip)" in data):
            keyboard_list.append([InlineKeyboardButton(
                text=get_text('buts.premium_course'),
                callback_data="more_about_course"
            )])

        if pay_list[buy_type]["skip_buy_handler"]:
            keyboard_list.append([InlineKeyboardButton(
                text=get_text("buts.back"),
                callback_data="call_profile"
            )])
        else:
            keyboard_list.append([InlineKeyboardButton(
                text=get_text("buts.back"),
                callback_data=f"choose_premium:{type}"
            )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def premium_course():
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text = get_text("buts.premium_course"),
            callback_data= "premium_course"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def crypto_currency(buy_type: str):
        keyboard_list = []
        for currency in config["CryptoCurrency"]:
            keyboard_list.append([InlineKeyboardButton(
                text=currency,
                callback_data= f'{buy_type}_{currency}')])
        if pay_list[buy_type.replace("crypto_", "")]["skip_buy_handler"]:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text("buts.back"),
                callback_data= "call_profile"
            )])
        else:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text("buts.back"),
                callback_data= "back_to_premium"
            )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def buy_handler(buy_type):
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.crypto"),
            callback_data= f"crypto_{buy_type}")])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.yoomoney"),
            callback_data= f"ym_{buy_type}")])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.manager"),
            url= config["ManagerLink"])])
        if pay_list[buy_type]["skip_buy_handler"]:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text("buts.back"),
                callback_data= "call_profile"
            )])
        else:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text("buts.back"),
                callback_data= "back_to_premium"
            )])
        return InlineKeyboardMarkup(inline_keyboard= keyboard_list)


    def pay(callback, url, amount):
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text=f"{get_text('buts.pay_link')}{amount}р.",
            web_app=WebAppInfo(url=url))])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def stable(pic_code: str):
        builder = InlineKeyboardBuilder()

        builder.button(
            text="🔭 Upscale",
            callback_data=f"upscale_{pic_code}"
        )

        builder.button(
            text="💫 Повторить",
            callback_data=f"retry_{pic_code}"
        )

        builder.button(
            text="⚙️ Меню",
            callback_data="manage_stable_menu_new"
        )

        builder.adjust(2, 1)
        return builder.as_markup()


    def stable_menu():
        builder = InlineKeyboardBuilder()

        builder.button(
            text="⚙️ Меню",
            callback_data="manage_stable_menu_new"
        )

        return builder.as_markup()


    def read_keyboard(keyboard: InlineKeyboardMarkup, action):
        keyboard_list = []
        for string in keyboard.inline_keyboard:
            temp_list = []
            for button in string:
                if button.callback_data == "pass" or button.callback_data == action:
                    text = "💫"
                    callback_data = "pass"
                else:
                    text = button.text
                    callback_data = button.callback_data
                temp_list.append(InlineKeyboardButton(
                    text= text,
                    callback_data= callback_data))
            keyboard_list.append(temp_list)
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def auto_confirm():
        keyboard_list = []

        keyboard_list.append([InlineKeyboardButton(
            text=f"✅ Да, я хочу отключить автоподписку",
            callback_data="disable_autoup_off"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.back"),
            callback_data="call_profile"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)

    def submgr(sub, buytype):
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text=f"❌ Отключить автопродление",
            callback_data=f"submgr_disable:{sub}:{buytype}"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text=f"⚡️ Назад",
            callback_data=f"call_profile"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def switch_to_stable():
        builder = InlineKeyboardBuilder()

        builder.button(
            text="⚙️ Настроить Stable Diffusion",
            callback_data="manage_stable_menu"
        )

        return builder.as_markup()


    def manage_stable(stable_ratio: str):
        builder = InlineKeyboardBuilder()

        builder.button(
            text="🏙️ Формат",
            callback_data="manage_stable_ratio"
        )

        builder.button(
            text="🧢 Стиль",
            callback_data="manage_stable_style"
        )

        builder.adjust(2)
        return builder.as_markup()


    def manage_ratio(ratio: str):
        builder = InlineKeyboardBuilder()

        button_list = [
            ("1024:1024", "1:1"),
            ("512:768", "2:3"),
            ("768:512", "3:2")
        ]

        for button in button_list:
            if ratio == button[0]:
                call_text = "✨ " + button[1]
                callback_data = "pass"
            else:
                call_text = button[1]
                callback_data = f"choise_ratio_{button[0]}"

            builder.button(
                text=call_text,
                callback_data=callback_data
            )

        builder.button(
            text="💫 Назад",
            callback_data="manage_stable_menu"
        )

        builder.adjust(1)
        return builder.as_markup()


    def manage_style(style: str):
        builder = InlineKeyboardBuilder()

        button_list = [
            ("Без стиля", "default"),
            ("Midjourney", "midjourney")
        ]

        for button in button_list:
            if style == button[1]:
                call_text = "✨ " + button[0]
                callback_data = "pass"
            else:
                call_text = button[0]
                callback_data=f"choise_style_{button[1]}"

            builder.button(
                text=call_text,
                callback_data=callback_data
            )

        builder.button(
            text="💫 Назад",
            callback_data="manage_stable_menu"
        )

        builder.adjust(1)
        return builder.as_markup()


    def manage_model(model: str):
        builder = InlineKeyboardBuilder()

        for key, value in MODELS_STABLE.items():
            if model == key:
                call_text = "✨ " + value.get('first_name')
                callback_data = "pass"
            else:
                call_text = value.get('first_name')
                callback_data = f"choise_model_{key}"

            builder.button(
                text=call_text,
                callback_data=callback_data
            )

        builder.button(
            text="💫 Назад",
            callback_data="manage_stable_menu"
        )

        builder.adjust(1)
        return builder.as_markup()
