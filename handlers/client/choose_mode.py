from aiogram.types import (Message, CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

from utils.func import get_text, stable_formatted
from config_data.config import MODELS_STABLE
from database.models.stable import Stable
from database.models.clients import Clients
from keyboards.client_kb import kb


async def panel_mode(message: Message, user: Clients):
    if user.model == "stable":
        await message.answer(
            text=get_text('text.generate_mj'),
            reply_markup=kb.panel_mode(message.from_user.id)
        )

    elif user.model == "chatgpt":
        await message.answer(
            text=get_text('text.generate_gpt'),
            reply_markup=kb.panel_mode(message.from_user.id)
        )

    elif user.model == "pikalabs":
        await message.answer(
            text=get_text('text.generate_zeroscope'),
            reply_markup=kb.panel_mode(message.from_user.id)
        )

    elif user.model == "deepai":
        await message.answer(
            text="<b>Выбран режим: 👨‍🎨 DeepAi</b>",
            reply_markup=kb.panel_mode(message.from_user.id)
        )

    elif user.model == "dalle":
        await message.answer(
            text="<b>Выбран режим: 👨‍🎨 DALL-E</b>",
            reply_markup=kb.panel_mode(message.from_user.id)

        )


async def choose_mode(call: CallbackQuery, state: FSMContext, user: Clients):
    if call.data == 'change_mode':
        await call.message.edit_text(
            text=get_text('text.change_mode_sms'),
            reply_markup= kb.change_mode(call.from_user.id)
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
            reply_markup=kb.switch_to_stable(call.from_user.id)
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
    TEXT = "<b>🏙️ Формат:</b> <code>{}</code>\n🧢 <b>Стиль:</b> <code>{}</code>".format(
            stable_formatted(stable.ratio, call.from_user.id),
            stable_formatted(stable.style)
    )

    if call.data == "manage_stable_menu_new":
        await call.message.answer(
            text=TEXT,
            reply_markup=kb.manage_stable(stable.ratio, call.from_user.id)
        )
    else:
        await call.message.edit_text(
            text=TEXT,
            reply_markup=kb.manage_stable(stable.ratio, call.from_user.id)
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
        reply_markup=kb.manage_ratio(stable.ratio, call.from_user.id)
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
        reply_markup=kb.manage_style(stable.style, call.from_user.id)
    )


async def manage_stable_model(call: CallbackQuery, stable: Stable):
    if call.data != "manage_stable_model":
        stable_model = call.data.split("_")[2]
        stable.model = stable_model

    call_text = MODELS_STABLE.get(stable.model).get('description')

    await call.message.edit_text(
        text=call_text,
        reply_markup=kb.manage_model(stable.model, call.from_user.id)
    )
