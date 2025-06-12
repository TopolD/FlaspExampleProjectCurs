from datetime import date, timedelta
from typing import Any
from sqlalchemy import and_, select, func, insert, or_
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDao
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.exceptions import AbsentBooking
from app.hotels.rooms.models import Rooms
from app.logger import log


class BookingDao(BaseDao):
    model = Bookings

    @classmethod
    async def add_booking(
            cls, user_id: int, room_id: int, date_from: date, date_to: date
    ) -> Any | None:
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(and_(Bookings.date_from < date_to,
                                Bookings.date_to > date_from))
                    .subquery()
                    .alias("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()

                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,

            }
            log.error(msg, extra=extra, exc_info=True)


    @classmethod
    async def get_user_bookings(cls, user_id: int):
        async with async_session_maker() as session:
            bookings = (
                select(
                    Bookings,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .join(Rooms, Rooms.id == Bookings.room_id)
                .where(Bookings.user_id == user_id)
            )
            bookings = await session.execute(bookings)
            bookings = bookings.mappings().all()
            return bookings

    @classmethod
    async def delete_booking(cls, id, user_id: int):
        async with async_session_maker() as session:
            bookings = select(Bookings).where(
                and_(Bookings.user_id == user_id, Bookings.id == id)
            )
            bookings = await session.execute(bookings)
            bookings = bookings.scalar()

            if not bookings:
                raise AbsentBooking

            await session.delete(bookings)
            await session.commit()

    @classmethod
    async def get_bookings_for_remainder(cls):
        async with async_session_maker() as session:
            today = date.today()
            all_bookings = select(Bookings.user_id,Bookings.date_from,Bookings.date_to).filter(
                or_(
                    Bookings.date_from == today + timedelta(days=1),
                    Bookings.date_from == today + timedelta(days=3)
                )
            )
            all_bookings = await session.execute(all_bookings)

            all_bookings = all_bookings.mappings().all()
            return all_bookings