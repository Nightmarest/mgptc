from aiogram import F, Router, Dispatcher
from aiogram.filters import StateFilter, ChatMemberUpdatedFilter, KICKED, MEMBER

from sqlalchemy.ext.asyncio import async_sessionmaker

from handlers.client.neural.dalle import dalle_image
from services import agreement
from utils.check_sub import c_listener
from config_data.config import config
from config_data.create_bot import db
from utils.func import get_text
from filters.states.state import ClientState
from handlers.admin.state import PromoState
from middlewares import SessionMiddleware, MediaGroupMiddleware
from filters.client import (
    GPTUserPoorFilter, MJUserPoorFilter, CheckSubFilter,
    MJRequestsToday, PikaLabsSUserPoorFilter, DeepAIUserPoorFilter,
    StableModelFilter, ChatGPTModelFilter, PikaLabsModelFilter, DeepAIModelFilter, DALLEUserPoorFilter, DALLEModelFilter
)
from handlers.client.client import (
    command_start, help, warning_in_progress,
    warning_user_poor, call_warning_in_progress, call_warning_user_poor,
    warning_check_sub, call_warning_check_sub, limit_requests_today,
    call_limit_requests_today, call_pass, user_blocked_bot, user_unblocked_bot
)
from handlers.client.profile import call_profile, profile, switch_voice_answer
from handlers.client.choose_mode import (
    panel_mode, choose_mode, manage_stable_menu,
      manage_stable_model, manage_stable_ratio, manage_stable_style
)
from handlers.client.neural.stable import stable_prompt, stable_upscale, stable_retry
from handlers.client.neural.chatgpt import chatgpt_text, chatgpt_voice
from handlers.client.neural.pikalabs import pikalabs_prompt
from handlers.client.neural.deepai import deepai_image
from handlers.client.buy_handler import (
    buy_handler, ym_check_payment, crypto_check_payment, choose_pay_ym,
    choose_pay_crypto, premium, call_premium, crypto_currency, description_premium,
    more_about_course, choose_premium, disable_autoup, disable_autoup_off, promocodes
)


def register_client_handlers(router: Router):
    # PAY HANDLERS
    router.callback_query.register(description_premium, F.data.startswith("description_"))
    router.callback_query.register(more_about_course, F.data == "more_about_course")
    router.callback_query.register(buy_handler, F.data.in_({"buy-0", "buy-1", "buy-2", "buy-3", "buy-4", "buy-5"}))
    router.callback_query.register(ym_check_payment, F.data.startswith("check_"), F.data.contains("ym"))
    router.callback_query.register(crypto_check_payment, F.data.startswith("check_"), F.data.contains("crypto"))
    router.callback_query.register(choose_pay_ym, F.data.startswith("ym"))
    router.callback_query.register(choose_pay_crypto, F.data.startswith("crypto"), F.data.split("_")[2].in_(config["CryptoCurrency"]))
    router.callback_query.register(crypto_currency, F.data.startswith("crypto"))
    router.callback_query.register(call_premium, F.data == "back_to_premium")
    router.callback_query.register(disable_autoup, F.data == "disable_autoup")
    router.callback_query.register(disable_autoup_off, F.data == "disable_autoup_off")

    # GENERAL HANDLERS
    router.my_chat_member.register(user_blocked_bot, ChatMemberUpdatedFilter(member_status_changed=KICKED), F.chat.type == "private")
    router.my_chat_member.register(user_unblocked_bot, ChatMemberUpdatedFilter(member_status_changed=MEMBER), F.chat.type == "private")

    router.callback_query.register(c_listener, F.data == 'subcheck') # ОП
    router.callback_query.register(call_profile, F.data == "call_profile")
    router.callback_query.register(switch_voice_answer, F.data == 'switch_voice_answer')
    router.callback_query.register(choose_premium, F.data.startswith("choose_premium"))
    router.message.register(command_start, F.text.startswith("/start"))          # Command /start
    router.message.register(command_start, F.text == get_text("buts.restart")) # <----|
    router.message.register(agreement.agreement_ok, F.text == get_text("buts.agreement_ok"))
    router.message.register(help, F.text == get_text("buts.help"))
    router.message.register(profile, F.text == get_text("buts.profile"))
    router.message.register(promocodes, F.text == get_text("buts.premium"))
    router.message.register(premium, StateFilter(PromoState.promo))



    router.callback_query.register(call_warning_in_progress, StateFilter(ClientState.process))
    router.message.register(warning_in_progress, StateFilter(ClientState.process))
    router.message.register(panel_mode, F.text == get_text("buts.choise_mode"))
    router.callback_query.register(choose_mode, F.data.endswith("_mode"))

    # FILTERS IN PROGRESS AND CHECK SUB
    router.message.register(warning_check_sub, CheckSubFilter())
    router.callback_query.register(call_warning_check_sub, CheckSubFilter())

    router.message.register(warning_user_poor, GPTUserPoorFilter(), ChatGPTModelFilter())
    router.message.register(warning_user_poor, MJUserPoorFilter(), StableModelFilter())
    router.message.register(warning_user_poor, PikaLabsSUserPoorFilter(), PikaLabsModelFilter())

    router.callback_query.register(call_warning_user_poor, GPTUserPoorFilter(), ChatGPTModelFilter())
    router.callback_query.register(call_warning_user_poor, MJUserPoorFilter(), StableModelFilter())
    router.message.register(call_warning_user_poor, PikaLabsSUserPoorFilter(), PikaLabsModelFilter())
    router.message.register(call_warning_user_poor, DeepAIUserPoorFilter(), DeepAIModelFilter())

    router.message.register(limit_requests_today, MJRequestsToday(), StableModelFilter())
    router.callback_query.register(call_limit_requests_today, MJRequestsToday(), StableModelFilter())
    router.callback_query.register(manage_stable_menu, F.data.startswith("manage_stable_menu"))
    router.callback_query.register(manage_stable_ratio, F.data == "manage_stable_ratio")
    router.callback_query.register(manage_stable_ratio, F.data.startswith("choise_ratio_"))
    router.callback_query.register(manage_stable_style, F.data == "manage_stable_style")
    router.callback_query.register(manage_stable_style, F.data.startswith("choise_style_"))
    router.callback_query.register(manage_stable_model, F.data == "manage_stable_model")
    router.callback_query.register(manage_stable_model, F.data.startswith("choise_model_"))

    router.message.register(stable_prompt, F.text, StableModelFilter())
    router.callback_query.register(stable_upscale, StableModelFilter(), F.data.startswith("upscale_"))
    router.callback_query.register(stable_retry, StableModelFilter(), F.data.startswith("retry_"))
    router.message.register(pikalabs_prompt, PikaLabsModelFilter(), F.text)
    router.message.register(deepai_image, DeepAIModelFilter(), F.photo)
    router.message.register(chatgpt_text, ChatGPTModelFilter(), F.text)
    router.message.register(chatgpt_voice, ChatGPTModelFilter(), F.voice)
    router.callback_query.register(call_pass, F.data == "pass")
    router.message.register(warning_user_poor, DALLEUserPoorFilter(), DALLEModelFilter())

    router.message.register(dalle_image, DALLEModelFilter(), F.text)


def register_middlewares(dp: Dispatcher, sessionmaker: async_sessionmaker):
    dp.update.outer_middleware(MediaGroupMiddleware())
    dp.update.outer_middleware(SessionMiddleware(sessionmaker))
