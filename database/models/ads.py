from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class Advertising(Base):
    __tablename__ = "ads"

    id: Mapped[str] = mapped_column(primary_key=True)
    token: Mapped[str]
    count: Mapped[int] = mapped_column(default=0)