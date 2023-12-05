from sqlalchemy.orm import Mapped, mapped_column
from . import Base
from .base import bigint

from config_data.config import MODELS_STABLE


class Stable(Base):
    __tablename__ = "stable"

    user_id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)

    model: Mapped[str] = mapped_column(default=list(MODELS_STABLE)[0])
    ratio: Mapped[str] = mapped_column(default="1024:1024")
    style: Mapped[str] = mapped_column(default="midjourney")
