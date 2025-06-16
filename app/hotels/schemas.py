from typing import List

from pydantic import BaseModel,ConfigDict


class SHotels(BaseModel):

    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)

class SNewHotels(BaseModel):

    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int


class SHotelsInfo(BaseModel):
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int