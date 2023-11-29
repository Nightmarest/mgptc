from typing import Any, Awaitable, Callable, Dict, Optional
from aiogram import BaseMiddleware
from aiogram.types import Update, User
from sqlalchemy.orm import Session
from sqlalchemy import select

from config_data.create_bot import db
from database.models.clients import Clients
from database.models.stable import Stable


class SessionMiddleware(BaseMiddleware):
    """
    Middleware for adding await session.
    """

    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        event_user: Optional[User] = data.get("event_from_user")

        async with self.sessionmaker() as session:
            async with session.begin():
                session: Session
                user = await session.scalar(
                    select(Clients)
                    .where(Clients.id == event_user.id)
                )

                stable = await session.scalar(
                    select(Stable)
                    .where(Stable.user_id == event_user.id)
                )

                if stable is None:
                    new_stable = Stable(
                        user_id=event_user.id
                    )
                    await session.merge(new_stable)
                    stable = await session.scalar(
                        select(Stable)
                        .where(Stable.user_id == event_user.id)
                    )

                data["session"] = session
                data["stable"] = stable
                data["user"] = user

                return await handler(event, data)
