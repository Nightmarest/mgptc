import logging as lg
import re
from typing import Union, Any
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select, delete

from config_data.config import config
from database.models import Base, Stack, Clients, Advertising, Promocodes


class PostgreSQL:
    def __init__(self):
        try:
            self.engine = create_engine(
                    URL(
                        'postgresql+psycopg2',
                        username=config["DBUser"],
                        password=config["DBPswd"],
                        host=config["DBHost"],
                        port=config["DBPort"],
                        database=config["DBName"],
                        query={},
                    ),
                    future=True,
                    pool_pre_ping=True
                )
            self.Session = sessionmaker(bind=self.engine)

            Base.metadata.create_all(bind=self.engine)
            lg.info("SYSTEM - Connection to database complete")
        except Exception as e:
            lg.error(f"ERROR - Can't establish connection to database: {e}")


    # Запись нового пользователя -> clients
    def recording(self, chat_id, name="", where_from="") -> None:
            try:
                with self.Session() as session:
                    if not session.query(Clients).filter(Clients.id == chat_id).first():
                        new_client = Clients(
                            id=chat_id,
                            name=name,
                            where_from=where_from
                        )
                        session.add(new_client)
                        session.commit()
            except Exception as e:
                lg.error(f"Error in recording: {e}")


    # Проверка на нового пользователя
    def is_new(self, chat_id: int) -> bool:
            try:
                with self.Session() as session:
                    client = session.query(Clients).filter(Clients.id == chat_id).first()
                    return client is None
            except Exception as e:
                lg.error(f"Error in is_new: {e}")


    # Обновить запись
    def update(self, chat_id: int, column: str, value: Union[int, str, bool]) -> None:
            try:
                with self.Session() as session:
                    client = session.query(Clients).filter(Clients.id == chat_id).first()
                    if client:
                        setattr(client, column, value)
                        session.commit()
            except Exception as e:
                lg.error(f"Error in update: {e}")


    # Получить запись
    def read(self, chat_id: int, column: str) -> Any:
            try:
                with self.Session() as session:
                    client = session.query(Clients).filter(Clients.id == chat_id).first()
                    if client:
                        return getattr(client, column)
            except Exception as e:
                lg.error(f"Error in read: {e}")
                return "None"


    def add_count_ads(self, ref_token: str) -> None:
            try:
                with self.Session() as session:
                    ref = session.scalar(
                        select(Advertising)
                        .where(Advertising.token == ref_token)
                    )
                    if not ref:
                        return

                    ref.count += 1
                    session.commit()
            except Exception as e:
                lg.error(f"Error in add_count_ads: {e}")


    # Добавление в СТЕК
    def stack_record(self, chat_id: int, prompt: str) -> None:
        try:
            with self.Session() as session:
                new_stack = Stack(
                    user_id=chat_id,
                    prompt=prompt
                )
                session.merge(new_stack)
                session.commit()
        except Exception as e:
            lg.error(f'stack_record error -> {e}')


    # Удалить запись из СТЕКА
    def delete_record(self, chat_id: int) -> None:
        try:
            with self.Session() as session:
                session.execute(
                    delete(Stack)
                    .where(Stack.user_id == chat_id)
                )
        except Exception as e:
            lg.error(f'delete record error -> {e}')


    # поиск промпта по стеку
    def search_prompt(self, search_prompt: str) -> None:
        #search_prompt = re.sub(r'<[^>]*>', '', search_prompt).strip()

        try:
            with self.Session() as session:
                user_id = session.scalar(
                    select(Stack.user_id)
                    .where(Stack.prompt == search_prompt)
                )

            return user_id
        except Exception as e:
            lg.error(f"error in search_prompt: {e}")
            return None


    def add_ads(self, name: str, token: str) -> None:
        try:
            with self.Session() as session:
                new_ads = Advertising(
                    id=name,
                    token=token
                )
                session.add(new_ads)
                session.commit()
        except Exception as e:
            lg.error(f"Error in add_ads: {e}")


    def delete_ads(self, token: str) -> None:
        try:
            with self.Session() as session:
                session.execute(
                    delete(Advertising)
                    .where(Advertising.token == token)
                )
                session.commit()
        except Exception as e:
            lg.error(f"Error in delete_ads: {e}")


    def admin_request(self, request: str) -> Any:
        try:
            with self.Session() as session:
                result = session.execute(text(request))
                return result.fetchall()
        except Exception as e:
            lg.error(f"Error in go: {e}")

    def recording_promo(self, promo, discount, uses) -> None:
            try:
                with self.Session() as session:
                        new_promo = Promocodes(
                            name=str(promo),
                            discount=int(discount),
                            uses=int(uses),
                            used=1
                        )
                        session.add(new_promo)
                        session.commit()
            except Exception as e:
                lg.error(f"Error in recording: {e}")

    def readpromo(self, promo: str) -> Any:
            try:
                with self.Session() as session:
                    promo = session.query(Promocodes).filter(Promocodes.name == promo).first()
                    if promo:
                        return promo
            except Exception as e:
                lg.error(f"Error in read: {e}")
                return "None"

    def conn(self):
        return self.Session