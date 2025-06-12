import asyncio
from datetime import date

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery_app
from app.tasks.email_tamplates import create_remainder_confirmation_template

import smtplib

from app.bookings.dao import BookingDao
from app.users.dao import UsersDao
from app.hotels.dao import HotelDao
from app.hotels.rooms.dao import RoomsDao


async def fetch_bookings_and_user():
    remainder_booking = await BookingDao.get_bookings_for_remainder()
    bookings = [dict(booking) for booking in remainder_booking]
    print(bookings)
    if not bookings:
        return [], None


    for booking in bookings:
        if isinstance(booking.get('date_from'), date):
            booking['date_from'] = booking['date_from'].strftime("%Y-%m-%d")
        if isinstance(booking.get('date_to'), date):
            booking['date_to'] = booking['date_to'].strftime("%Y-%m-%d")
    user = await UsersDao.find_by_id(bookings[0]['user_id'])
    return bookings, user.email


@celery_app.task(name="remainder_task")
def periodic_remainder_task():
    bookings, user = asyncio.run(fetch_bookings_and_user())
    if bookings and user:
            remainder_bookings.delay(bookings)


@celery_app.task()
def remainder_bookings(
        bookings,
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_remainder_confirmation_template(bookings, email_to_mock)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        if not msg_content:
            raise RuntimeError("Ошибка генерации письма: содержимое отсутствует.")
        for email in msg_content:
            server.send_message(email)
