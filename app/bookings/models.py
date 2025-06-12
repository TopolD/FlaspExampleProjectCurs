from datetime import date

from sqlalchemy import ForeignKey, Date, Computed, Integer
from sqlalchemy.orm import Mapped,relationship
from sqlalchemy.testing.schema import mapped_column

from app.database import Base



class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"),nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Integer,Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Integer,Computed("date_to - date_from"))

    room : Mapped["Rooms"] =  relationship( back_populates="booking")
    user : Mapped["Users"]  = relationship( back_populates="booking")


    def __str__(self):
        return f"Booking: id={self.id}, room_id={self.room_id}, user_id={self.user_id}, date_from={self.date_from}, date_to={self.date_to}, price={self.price}"