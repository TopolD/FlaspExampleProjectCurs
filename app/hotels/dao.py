from datetime import date
from sqlalchemy import and_, select, func
from app.bookings.models import Bookings
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDao(BaseDao):
    model = Hotels

    @classmethod
    async def find_by_location(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            busy_booked_rooms = select(Rooms.hotel_id.label('Hotel_id'),
                func.count('*').label('booked_count')).select_from(Rooms, Bookings
                ).join(Rooms, Rooms.id == Bookings.room_id).where(
                and_(
                    Bookings.date_from < date_to,
                    Bookings.date_to > date_from,
                )
            ).group_by(Rooms.hotel_id).subquery().alias('busy_booked_rooms')

            rooms_quantity = select(
                Hotels.name,
                Hotels.location,
                Hotels.services,
                (Hotels.rooms_quantity - func.coalesce(select(busy_booked_rooms.c.booked_count).where(
                    Hotels.id == busy_booked_rooms.c.Hotel_id).scalar_subquery(), 0)).label(
                    "rooms_quantity"),
                Hotels.image_id
            ).where(Hotels.location.like(f'%{location}%'))

            rooms_quantity = await session.execute(rooms_quantity)
            rooms_quantity = rooms_quantity.mappings().all()

            return rooms_quantity

    @classmethod
    async def get_list_rooms(cls, hotel_id, date_from: date, date_to: date):
        async with (async_session_maker() as session):
            booked_rooms = select(Bookings.total_days, func.count('*').label('total'
                                                                             )).select_from(Bookings).join(Rooms,
                                                                                                           Rooms.id == Bookings.room_id).where(
                and_(Rooms.id == hotel_id,
                     and_(
                         Bookings.date_from < date_to,
                         Bookings.date_to > date_from,
                     ))).group_by(Bookings.id).subquery().alias('booked_rooms')

            list_rooms = select(
                Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, Rooms.price, Rooms.services, Rooms.image_id,
                func.coalesce(Rooms.price * select(booked_rooms.c.total_days).scalar_subquery(), Rooms.price).label(
                    'total_cost'),
                func.coalesce(Rooms.quantity - select(booked_rooms.c.total).scalar_subquery(), Rooms.quantity).label(
                    'rooms_left')
            ).where(Rooms.id == hotel_id)

            list_rooms = await session.execute(list_rooms)
            list_rooms = list_rooms.mappings().all()

            return list_rooms


# import asyncio
#
#
# #
# #
# async def example_by_location():
#     location = 'Алтай'
#     date_from = date(2023, 6, 15)
#     date_to = date(2023, 6, 30)
#     result = await HotelDao.find_by_location(location, date_from, date_to)
#     print(result)


# async def example_list_rooms():
#     hotel_id = 3
#     date_from = date(2023, 5, 15)
#     date_to = date(2023, 6, 20)
#     result = await HotelDao.get_list_rooms(hotel_id, date_from, date_to)
#     print(result)
#
# #
# asyncio.run(example_by_location())
