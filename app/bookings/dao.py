from datetime import date

from sqlalchemy import and_, select, or_, func, insert

from app.dao.base import BaseDao
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDao(BaseDao):
    model = Bookings

    @classmethod
    async def get_booked_rooms(cls, room_id, date_from: date, date_to: date):
        booked_rooms = select(Bookings).where(
            and_(
                Bookings.date_from < date_to,
                Bookings.date_to > date_from,
            )
        )
        return booked_rooms

    @classmethod
    async def get_rooms_left(cls, room_id, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = await cls.get_booked_rooms(room_id, date_from, date_to)

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(Rooms).join(
                Rooms.id == booked_rooms.c.room_id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            get_rooms_left = await session.execute(get_rooms_left)
            get_rooms_left = get_rooms_left.scalar()

        return get_rooms_left

    @classmethod
    async def add(cls, room_id, date_from: date, date_to: date, user_id: int):
        async with async_session_maker() as session:
            rooms_left = await cls.get_rooms_left(room_id, date_from, date_to)

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None
