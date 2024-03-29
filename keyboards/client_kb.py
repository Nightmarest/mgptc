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
from config_data.create_bot import db


class kb:
    def choose_lang():
        keyboard_list = []

        keyboard_list.append([InlineKeyboardButton(
            text="🇷🇺 Русский",
            callback_data="setlang:ru"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text="🇺🇸 English",
            callback_data="setlang:en"
        )])

        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def langinstalled(id):
        b1 = KeyboardButton(text = get_text("buts.Continue", id))
        kb_langc = ReplyKeyboardMarkup(
            row_width=1, resize_keyboard=True,
            one_time_keyboard = True, keyboard = [[b1]]
        )

        return kb_langc
    # Start Keyboard
    def start_agreement(id):
        b1 = KeyboardButton(text = get_text("buts.agreement_ok", id))
        kb_agreement = ReplyKeyboardMarkup(
            row_width=1, resize_keyboard=True,
            one_time_keyboard = True, keyboard = [[b1]]
        )

        return kb_agreement
    def start(id):
        b1 = KeyboardButton(text = get_text("buts.choise_mode", id))
        b2 = KeyboardButton(text = get_text("buts.help", id))
        b3 = KeyboardButton(text = get_text("buts.profile", id))
        # b4 = KeyboardButton(text = get_text("buts.premium"))
        b4 = KeyboardButton(text = get_text("buts.restart", id))

        kb_start = ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True, one_time_keyboard=False,
            keyboard=[[b1, b3],
                      [b2, b4]

            ]
        )
        return kb_start


    def panel_mode(id):
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text = get_text('buts.change_mode', id),
            callback_data= 'change_mode'
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def profile(premium_type: str, course: bool, voice_answer: bool, auto: bool, autov2: bool, id: int):
        if premium_type:
            query_menu = pay_list[premium_type]["menu_prompt"]
        else:
            query_menu = False
        if voice_answer:
            voice_text = get_text('buts.voice_text_on', id)
        else:
            voice_text = get_text('buts.voice_text_off', id)
        keyboard_list = []

        if course:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text('buts.profile_education', id),
                url= config["EducationUrl"]
            )])
        else:
            keyboard_list.append([InlineKeyboardButton(
                text = get_text('buts.profile_education', id),
                callback_data= "description_buy-3_buy-3"
            )])

        keyboard_list.append([InlineKeyboardButton(
            text = get_text('buts.profile_forum', id),
            url = config["ForumUrl"]
        )])

        keyboard_list.append([InlineKeyboardButton(
            text=voice_text,
            callback_data="switch_voice_answer"
        )])

        if auto is True:
            keyboard_list.append([InlineKeyboardButton(
                text=get_text("buts.autoup", id),
                callback_data="disable_autoup"
            )])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.AnotherLang", id),
            callback_data="getlang"
        )])

        # keyboard_list.append([InlineKeyboardButton(
        #     text="Отключить предыдущие подписки",
        #     callback_data="disable_autoup_recursive"
        # )])

        if autov2 is True:
            keyboard_list.append([InlineKeyboardButton(
                text=get_text("buts.SubManage", id),
                callback_data="disable_autoups"
            )])


        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def change_mode(id):
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
        #keyboard_list.append([InlineKeyboardButton(
        #    text = "DALL-E",
        #    callback_data="dalle_mode"
        #)])
        keyboard_list.append([InlineKeyboardButton(
            text = "DeepAI",
            callback_data="deepai_mode"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def back_to_profile(id):
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text = get_text("buts.back", id),
            callback_data= "call_profile"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def pay_list_keyboard(type: str, auto: bool, id: int):
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
            text=get_text("buts.back", id),
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


    def stable(pic_code: str, id):
        builder = InlineKeyboardBuilder()

        builder.button(
            text="🔭 Upscale",
            callback_data=f"upscale_{pic_code}"
        )

        builder.button(
            text=get_text("buts.stable_retry", id),
            callback_data=f"retry_{pic_code}"
        )

        builder.button(
            text=get_text("buts.stable_menu", id),
            callback_data="manage_stable_menu_new"
        )

        builder.adjust(2, 1)
        return builder.as_markup()


    def stable_menu(id):
        builder = InlineKeyboardBuilder()

        builder.button(
            text=get_text("buts.stable_menu", id),
            callback_data="manage_stable_menu_new"
        )

        return builder.as_markup()


    def read_keyboard(keyboard: InlineKeyboardMarkup, action, id):
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


    def auto_confirm(id):
        keyboard_list = []

        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.disableautosubf", id),
            callback_data="disable_autoup_off"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.back", id),
            callback_data="call_profile"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)

    def submgr(sub, buytype, id):
        keyboard_list = []
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.disableautosub", id),
            callback_data=f"submgr_disable:{sub}:{buytype}"
        )])
        keyboard_list.append([InlineKeyboardButton(
            text=get_text("buts.back", id),
            callback_data=f"call_profile"
        )])
        return InlineKeyboardMarkup(inline_keyboard=keyboard_list)


    def switch_to_stable(id):
        builder = InlineKeyboardBuilder()

        builder.button(
            text=get_text("buts.SettingsStable", id),
            callback_data="manage_stable_menu"
        )

        return builder.as_markup()


    def manage_stable(stable_ratio: str, id):
        builder = InlineKeyboardBuilder()

        builder.button(
            text=get_text("buts.StableFormat", id),
            callback_data="manage_stable_ratio"
        )

        builder.button(
            text=get_text("buts.StableStyle", id),
            callback_data="manage_stable_style"
        )

        builder.adjust(2)
        return builder.as_markup()


    def manage_ratio(ratio: str, id):
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
            text=get_text("buts.back", id),
            callback_data="manage_stable_menu"
        )

        builder.adjust(1)
        return builder.as_markup()


    def manage_style(style: str, id):
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
            text=get_text("buts.back", id),
            callback_data="manage_stable_menu"
        )

        builder.adjust(1)
        return builder.as_markup()


    def manage_model(model: str, id):
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
            text=get_text("buts.back", id),
            callback_data="manage_stable_menu"
        )

        builder.adjust(1)
        return builder.as_markup()


