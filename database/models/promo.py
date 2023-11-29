from sqlalchemy.orm import Mapped, mapped_column
from .import Base


class Promocodes(Base):
    __tablename__ = "promo"

    name: Mapped[str] = mapped_column(primary_key=True)
    uses: Mapped[str]
    used: Mapped[str]
    discount: Mapped[int]
