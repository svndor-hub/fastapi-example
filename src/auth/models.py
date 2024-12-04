from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    disabled: Mapped[bool]
    hashed_password: Mapped[str]