from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column


from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services:  Mapped[dict] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]
