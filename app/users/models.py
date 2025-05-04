from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str]
