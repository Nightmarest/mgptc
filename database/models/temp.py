from sqlalchemy.orm import Mapped, mapped_column
from . import Base
from .base import bigint

class Temp(Base):
    __tablename__ = "temp"

    pic_code: Mapped[str] = mapped_column(primary_key=True)
    prompt: Mapped[str] = mapped_column(nullable=False)