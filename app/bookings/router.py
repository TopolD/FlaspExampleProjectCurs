from datetime import date

from fastapi import APIRouter
from fastapi.params import Depends

from app.bookings.dao import BookingDao
from app.exceptions import RoomCannotBeBooked, AbsentBooking

from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDao.get_user_bookings(user_id=user.id)


@router.post("")
async def add_booking(
        room_id: int,date_from:date,date_to:date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDao.add(room_id,date_from,date_to,user.id)
    if not booking:
        raise RoomCannotBeBooked


@router.delete("")
async def delete_booking(id: int,user: Users = Depends(get_current_user)):
    bookings = await BookingDao.find_by_id(id)
    if not bookings:
        raise AbsentBooking
    query_for_del = await BookingDao.dell(id)
