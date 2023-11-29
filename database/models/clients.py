from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from config_data.config import config
from . import Base
from .base import bigint


class Clients(Base):
    __tablename__ = "clients"

    id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(default="")
    people_ref: Mapped[int] = mapped_column(default=0)
    join_date: Mapped[date] = mapped_column(default=date.today())
    where_from: Mapped[str] = mapped_column(default="")
    dead: Mapped[bool] = mapped_column(default=False)

    model: Mapped[str] = mapped_column(default="stable")
    mj_images_count: Mapped[int] = mapped_column(default=0)
    requests_mj: Mapped[int] = mapped_column(default=config["StartFreeTokensMJ"])
    requests_gpt: Mapped[int] = mapped_column(default=config["StartFreeTokensGPT"])
    requests_mj_today: Mapped[int] = mapped_column(default=0)
    requests_pikalabs: Mapped[int] = mapped_column(default=config["StartFreeTokensGPT"])
    requests_deepai: Mapped[int] = mapped_column(default=config["StartFreeTokensGPT"])
    requests_dalle: Mapped[int] = mapped_column(default=5)


    buyer: Mapped[bool] = mapped_column(default=False)
    query_menu: Mapped[bool] = mapped_column(default=False)
    course: Mapped[bool] = mapped_column(default=False)
    voice_answer:  Mapped[bool] = mapped_column(default=False)
    premium_type: Mapped[str] = mapped_column(default="")
    premium_type_pika: Mapped[str] = mapped_column(default="")
    expired_time: Mapped[str] = mapped_column(default="")
    expired_time_pika: Mapped[str] = mapped_column(default="")

    premium_type_deepai: Mapped[str] = mapped_column(default="")
    expired_time_deepai: Mapped[str] = mapped_column(default="")


    invoiceid: Mapped[bigint] = mapped_column(default=0)
    cardtoken: Mapped[Optional[str]] = mapped_column(default="")
    subid: Mapped[Optional[str]] = mapped_column(default="")
    promo: Mapped[Optional[str]] = mapped_column(default="")
    agreement: Mapped[bool] = mapped_column(default=False)


    # mj_images_count = Column(Integer, default=0)
    # requests_mj = Column(Integer, default=10)
    # requests_gpt = Column(Integer, default=10)
    # requests_mj_today = Column(Integer, default=0)
    # requests_zeroscope = Column(Integer, default=10)

    # buyer = Column(Boolean, default=False)
    # query_menu = Column(Boolean, default=False)
    # course = Column(Boolean, default=False)
    # voice_answer = Column(Boolean, default=False)
    # premium_type = Column(String, default="")
    # expired_time = Column(String, default="")

    # invoiceid = Column(Integer)
    # cardtoken = Column(String)
    # subid = Column(String)
