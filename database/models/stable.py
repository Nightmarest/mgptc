from sqlalchemy.orm import Mapped, mapped_column
from . import Base
from .base import bigint

class Stable(Base):
    __tablename__ = "stable"

    user_id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)

    model: Mapped[str] = mapped_column(default="juggernaut-xl")
    ratio: Mapped[str] = mapped_column(default="1024:1024")
    style: Mapped[str] = mapped_column(default="midjourney")
