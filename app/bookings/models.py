from datetime import datetime

from sqlalchemy import ForeignKey, Date, Computed, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"),nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Integer,Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Integer,Computed("date_to - date_from"))
