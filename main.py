import asyncio

from handlers.register import register_client_handlers, register_middlewares
from handlers.admin.register import register_admin_hanlders
from database.engine import create_sessionmaker
from config_data.create_bot import (
    dp, bot, router_admin, router_client
)


async def main():
    sessionmaker = await create_sessionmaker()
    register_middlewares(dp, sessionmaker)

    dp.include_router(router_admin)
    register_admin_hanlders(router_admin)

    dp.include_router(router_client)
    register_client_handlers(router_client)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=['callback_query', 'message',
                                                 'inline_query', 'my_chat_member'])


if __name__ == "__main__":
    asyncio.run(main())
