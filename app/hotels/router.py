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


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, date_from: date, date_to: date) -> list[dict]:
    rooms = await HotelDao.get_list_rooms(hotel_id, date_from, date_to)
    return rooms


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    hotel = await HotelDao.find_by_id(id=hotel_id)
    return hotel

