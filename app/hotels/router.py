from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelDao

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)




@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[dict]:
    hotels = await HotelDao.find_by_location(location, date_from, date_to)
    return hotels
@router.get("")
async def get_hotels():
    return {"message": "Hello from hotels"}