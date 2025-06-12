from datetime import date

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_versioning import version
from pydantic import TypeAdapter

from app.bookings.dao import BookingDao
from app.bookings.dependencies import calculate_day
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked, AbsentBooking
from app.tasks.tasks import send_booking_confirmation_email

from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDao.get_user_bookings(user_id=user.id)


@router.post("/add")
@version(1)
async def add_booking(booking: SNewBooking, user: Users = Depends(get_current_user),):
    booking_obj = await BookingDao.add_booking(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )

    if not booking_obj:
        raise RoomCannotBeBooked
    calculate_day(booking.date_from,booking.date_to)
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    # send_booking_confirmation_email.delay(booking,user.email)
    return booking
@router.delete("/del")
async def delete_booking(id:int,user: Users = Depends(get_current_user)):
    query_for_del = await BookingDao.delete_booking(id,user.id)