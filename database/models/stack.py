from sqlalchemy.orm import Mapped, mapped_column
from . import Base
from .base import bigint

class Stack(Base):
    __tablename__ = "stack"

    user_id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)
    prompt: Mapped[str] = mapped_column(default="")
