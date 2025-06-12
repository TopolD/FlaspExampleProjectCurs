from typing import List

from pydantic import BaseModel,ConfigDict

class SRooms(BaseModel):

    hotel_id: int
    name: str
    description: str
    price: int
    services: List[str]
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)

class SNewRooms(BaseModel):

    hotel_id: int
    name: str
    description: str
    price: int
    services: List[str]
    quantity: int
    image_id: int


