import asyncio
from datetime import date, datetime

from sqlalchemy import and_, select, or_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms

"""
     использовать метод having 
     
     2 задача решена!!!! 
   with 
	
	booked_rooms  as( select total_days,count(*) as total  from bookings where room_id = 1 and (date_from >= '2023-05-15' and date_from <= '2023-06-20') or (date_from <= '2023-05-15' and date_to > '2023-05-15') group by 1  )




    select r.id, r.hotel_id , r.name, r.description , r.price, r.services , r.image_id ,  
    round(sum(r.price * (select total_days  from booked_rooms ))) as total_cost,
    round(sum(r.quantity - coalesce((select total from booked_rooms)))) as rooms_left
    from rooms r 
    join hotels h 
    on h.id = r.hotel_id
    where  r.id = 1
    group by r.id 
    
    3 задача  надо быть авторизованым 
    select b.*,r.name, r.description, r.services, r.image_id  from bookings b
        join rooms r 
        on r.id = b.room_id
        where b.room_id = 1 
"""


class HotelDao(BaseDao):
    model = Hotels

    @classmethod
    async def find_by_location(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:

            booked_rooms = select(Bookings.room_id,func.count('*').label('booked_count')).where(

                    and_(
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from,
                    )

            ).group_by(Bookings.room_id).subquery().alias('booked_rooms')





            rooms_quantity = select(
                Hotels.name,
                Hotels.location,
                Hotels.services,
                (Hotels.rooms_quantity - func.coalesce(select(booked_rooms.c.booked_count).scalar_subquery(), 0)).label("rooms_quantity"),
                Hotels.image_id
            ).where(Hotels.location.like(f'%{location}%'))

            rooms_quantity = await session.execute(rooms_quantity)
            rooms_quantity = rooms_quantity.mappings().all()

            return rooms_quantity


import asyncio


async def example():
    location = 'Алтай'
    date_from = date(2023, 5, 15)
    date_to = date(2023, 6, 20)
    result = await HotelDao.find_by_location(location, date_from, date_to)
    print(result)



asyncio.run(example())
