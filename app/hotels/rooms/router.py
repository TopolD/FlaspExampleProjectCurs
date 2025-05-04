from fastapi import APIRouter

from app.hotels.dao import HotelDao

router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"]
)



@router.get("/{hotel_id}/rooms")
async def get_rooms():
    return {"message": "Hello from rooms"}