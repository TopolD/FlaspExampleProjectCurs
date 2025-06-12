from datetime import datetime

from app.bookings.dao import BookingDao


async def test_add_and_get_booking():
    new_booking = await BookingDao.add(
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24","%Y-%m-%d"),
        user_id=2
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDao.find_by_id(new_booking.id)

    assert new_booking is not None



# async def test_bookings():
#     new_booking = await BookingDao.add(
#         room_id=2,
#         date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
#         date_to=datetime.strptime("2023-07-24","%Y-%m-%d"),
#         user_id=2
#     )
#     assert new_booking.user_id == 2
#     assert new_booking.room_id == 2
#     new_booking = await BookingDao.find_by_id(new_booking.id)
#     assert new_booking is not None
#
#
#
#     await BookingDao.delete_booking(new_booking.id,new_booking.user_id)
#
#     bookings = await BookingDao.find_by_id(new_booking.id)
#     assert bookings is None
