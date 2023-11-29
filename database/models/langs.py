from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class Language(Base):
    __tablename__ = "langs"

    index: Mapped[str] = mapped_column(primary_key=True)
    admin_name: Mapped[str] = mapped_column(nullable=False)

    rus: Mapped[str] = mapped_column(nullable=False)
    eng: Mapped[str] = mapped_column(nullable=False)
