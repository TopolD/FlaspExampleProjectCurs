import asyncio
from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Query
from fastapi.params import Depends
from pydantic import parse_obj_as, TypeAdapter

from app.bookings.dao import BookingDao
from app.exceptions import NoHotelHTTPException
from app.hotels.dao import HotelDao

from fastapi_cache.decorator import cache
from fastapi.params import Depends

from app.hotels.models import Hotels
from app.hotels.schemas import SNewHotels, SHotels, SHotelsInfo
from app.users.dependencies import get_current_user
from app.users.models import Users

from upstash_redis import AsyncRedis

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}")
):
    hotels = await HotelDao.find_by_location(location, date_from, date_to)

    return hotels



@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, date_from: date, date_to: date) -> list[dict]:
    rooms = await HotelDao.get_list_rooms(hotel_id, date_from, date_to)
    return rooms


@router.get("/id/{hotel_id}")
@cache(expire=60)
async def get_hotel_by_id(hotel_id: int):
    hotel = await HotelDao.find_by_id(id=hotel_id)
    return hotel

