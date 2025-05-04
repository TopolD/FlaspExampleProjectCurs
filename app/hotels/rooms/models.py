from sqlalchemy.types import JSON
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    services: Mapped[dict] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]
