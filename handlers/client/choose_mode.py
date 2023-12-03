from aiogram.types import (Message, CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

from utils.func import get_text, stable_formatted
from database.models.stable import Stable
from database.models.clients import Clients
from keyboards.client_kb import kb


async def panel_mode(message: Message, user: Clients):
    if user.model == "stable":
        await message.answer(
            text=get_text('text.generate_mj'),
            reply_markup=kb.panel_mode()
        )

    elif user.model == "chatgpt":
        await message.answer(
            text=get_text('text.generate_gpt'),
            reply_markup=kb.panel_mode()
        )

    elif user.model == "pikalabs":
        await message.answer(
            text=get_text('text.generate_zeroscope'),
            reply_markup=kb.panel_mode()
        )

    elif user.model == "deepai":
        await message.answer(
            text="<b>Выбран режим: 👨‍🎨 DeepAi</b>",
            reply_markup=kb.panel_mode()
        )
    elif user.model == "dalle":
        await message.answer(
            text="<b>Выбран режим: 👨‍🎨 DALL-E</b>",
            reply_markup=kb.panel_mode()

        )



async def choose_mode(call: CallbackQuery, state: FSMContext, user: Clients):
    if call.data == 'change_mode':
        await call.message.edit_text(
            text=get_text('text.change_mode_sms'),
            reply_markup= kb.change_mode()
        )

    elif call.data == 'chatgpt_mode':
        user.model = "chatgpt"
        await state.update_data(
            dialog_list=[{"role": "system", "content": ""}]
        )
        await call.message.edit_text(
            text=get_text('text.switch_to_chatgpt')
        )

    elif call.data == 'stable_mode':
        user.model = "stable"
        await call.message.edit_text(
            text=get_text('text.switch_to_midjourney'),
            reply_markup=kb.switch_to_stable()
        )

    elif call.data == 'pikalabs_mode':
        user.model = "pikalabs"
        await call.message.edit_text(
            text=get_text('text.switch_to_pikalabs')
        )

    elif call.data == 'deepai_mode':
        user.model = "deepai"
        await call.message.edit_text(
            text=get_text('text.switch_to_deepai')
        )
    elif call.data == 'dalle_mode':
        user.model = "dalle"
        await call.message.edit_text(
            text=get_text('text.switch_to_dalle')
        )




async def manage_stable_menu(call: CallbackQuery, stable: Stable):
    await call.answer()
    TEXT = "<b>🏙️ Формат:</b> <code>{}</code>\n🧢 <b>Стиль:</b> <code>{}</code>\n<b>🖱️ Модель:</b> <code>{}</code>".format(
            stable_formatted(stable.ratio),
            stable_formatted(stable.style),
            stable_formatted(stable.model)
    )

    if call.data == "manage_stable_menu_new":
        await call.message.answer(
            text=TEXT,
            reply_markup=kb.manage_stable(stable.ratio)
        )
    else:
        await call.message.edit_text(
            text=TEXT,
            reply_markup=kb.manage_stable(stable.ratio)
        )


async def manage_stable_ratio(call: CallbackQuery, stable: Stable):
    call_text = ""
    if call.data != "manage_stable_ratio":
        call_ratio = call.data.split("_")[2]
        stable.ratio = call_ratio

    if stable.ratio == "1024:1024":
        call_text = '''<a href="https://telegra.ph/file/0706eb11e9cde08ac3b22.jpg">⁠</a><b>Квадратный формат</b>'''

    elif stable.ratio == "512:768":
        call_text = '''<a href="https://telegra.ph/file/b5523204b71b2ba648c45.jpg">⁠</a><b>Портретный формат</b>'''

    elif stable.ratio == "768:512":
        call_text = '''<a href="https://telegra.ph/file/c436a96a1ab74192b4280.jpg">⁠</a><b>Широкий формат</b>'''

    await call.message.edit_text(
        text=call_text,
        reply_markup=kb.manage_ratio(stable.ratio)
    )


async def manage_stable_style(call: CallbackQuery, stable: Stable):
    call_text = ""

    if call.data != "manage_stable_style":
        call_style = call.data.split("_")[2]
        stable.style = call_style

    if stable.style == "midjourney":
        call_text = '''<a href="https://telegra.ph/file/8167c1d041e2188445427.png">⁠</a><b>Стиль Midjourney добавляет теплоты и делает изображение похожим на картину.</b>'''
    elif stable.style == "default":
        call_text = '''<a href="https://telegra.ph/file/4c8f99299558de0a1a617.png">⁠</a>Изображение без стиля, у вас полная свобода действий!🕊'''

    await call.message.edit_text(
        text=call_text,
        reply_markup=kb.manage_style(stable.style)
    )


async def manage_stable_model(call: CallbackQuery, stable: Stable):
    call_text = ""

    if call.data != "manage_stable_model":
        stable_model = call.data.split("_")[2]
        stable.model = stable_model

    text_list = [
        (
            f'''{hide_link("https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/c63c2f98-4d4a-43e8-82c4-f7a577a8db72/width=1152/00000-1447182128.jpeg")}<b>С помощью Juggernaut XL вы можете без особых усилий создавать реалистичных, кинематографичных и фотореалистичных персонажей и локации.

Рекомендуем в целом использовать эту модель, применяя стиль Midjourney.</b>''',
            "juggernaut-xl-v7"
        ),
        (
            f'''{hide_link("https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/68df5736-dd1f-4df4-8e7d-5fbd7adf8730/width=720/0.jpeg")}<b>Эта модель отлично настроена для фотореализма.</b>''',
            "albedobase-xl"
        ),
        (
            f'''{hide_link("https://image.stablediffusionapi.com/?quality=45&Image=https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/18141439221696749891.png")}<b>Эта модель не поддается ограничениям и дает вам возможность создавать все, что пожелает ваше воображение.</b>''',
            "yamermix-v8-vae"
        ),
        (
            f'''{hide_link("https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/18350195621701335828.png")}<b>Новая Colossus Project XL даёт революционные возможности создания изображений по коротким подсказкам. Уникальный набор данных и улучшенные алгоритмы позволяют с лёгкостью генерировать шедевры.</b>''',
            "colossus-project-xl-sfwns"
        )
    ]

    for text in text_list:
        if stable.model == text[1]:
            call_text = text[0]

    await call.message.edit_text(
        text=call_text,
        reply_markup=kb.manage_model(stable.model)
    )
