from aiogram import F, Router
from aiogram.filters import StateFilter
from config_data.config import config

from handlers.admin.state import (
    AdminState
)
from handlers.admin.admin import (
    admin_call_handler, admin_menu
)
from handlers.admin.mailling import (
    mailling, mailling_stop
)
from handlers.admin.text import (
    text_call_handler, update_text, update_text_done
)
from handlers.admin.sections.admin_link import (
    link_add_two, link_delete, link_add_one, link_stats
)
from handlers.admin.sections.admin_sub import (
    sub_call_handler, sub_channel_forwarded, sub_channel_url, sub_delete, sub_bot_token, sub_bot_url
)
from handlers.admin.commands import (
    check_user, increase_user, decrease_user, export_users, restart_bot
)


def register_admin_hanlders(router_admin: Router):
    router_admin.message.filter(F.chat.id.in_(config["AdminList"]))

    # MAILLING
    router_admin.message.register(mailling, StateFilter(AdminState.mail))
    router_admin.callback_query.register(mailling_stop, F.data == 'mail_stop')

    # MAIN MENU
    router_admin.message.register(admin_menu, F.text == '/admin')
    router_admin.callback_query.register(admin_call_handler, F.data.startswith("adm_"))

    # REF LINK
    router_admin.callback_query.register(link_stats, F.data.startswith("linkstat_"))
    router_admin.callback_query.register(link_add_one, F.data.startswith("link_"))
    router_admin.message.register(link_add_two, F.text, StateFilter(AdminState.link_add))
    router_admin.callback_query.register(link_delete, F.data.startswith("linkdelete_"))

    # ADMIN OP
    router_admin.callback_query.register(sub_call_handler, F.data.contains("sub_"))
    router_admin.message.register(sub_channel_forwarded, StateFilter(AdminState.sub_add_channel_1))
    router_admin.message.register(sub_channel_url, F.text, StateFilter(AdminState.sub_add_channel_2))
    router_admin.message.register(sub_delete, F.text, StateFilter(AdminState.sub_delete))
    router_admin.message.register(sub_bot_token, F.text, StateFilter(AdminState.sub_add_bot_1))
    router_admin.message.register(sub_bot_url, F.text, StateFilter(AdminState.sub_add_bot_2))

    # UPDATE TEXT
    router_admin.callback_query.register(text_call_handler, F.data.startswith("text"))
    router_admin.callback_query.register(update_text, F.data.startswith("update_text"))
    router_admin.message.register(update_text_done, F.text, StateFilter(AdminState.update_text))

    # КОМАНДЫ АДМИНА
    router_admin.message.register(check_user, F.text.contains('/проверить'))
    router_admin.message.register(increase_user, F.text.contains('/увеличить'))
    router_admin.message.register(decrease_user, F.text.contains('/уменьшить'))
    router_admin.message.register(export_users, F.text.contains('/выгрузка'))
    router_admin.message.register(restart_bot, F.text.contains('/restart'))