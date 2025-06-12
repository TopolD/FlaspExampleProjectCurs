from typing import Optional

from sqlalchemy.types import JSON
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column


from app.database import Base



class Rooms(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[dict] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    booking : Mapped[list["Bookings"]] =  relationship(back_populates="room")
    hotel : Mapped["Hotels"] =  relationship( back_populates="room")

    def __str__(self):
        return f"Room Room={self.name}"