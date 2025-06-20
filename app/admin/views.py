from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model = Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name= 'User'
    name_plural = 'Users'

class HotelsAdmin(ModelView, model = Hotels):
    column_list = [c.name for c in Hotels.__table__.c ] + [Hotels.room]
    name = 'Hotel'
    name_plural = 'Hotels'

class RoomsAdmin(ModelView, model = Rooms):
    column_list = [c.name for c in Rooms.__table__.c ] + [Rooms.hotel, Rooms.booking]
    name = 'Room'
    name_plural = 'Rooms'

class BookingsAdmin(ModelView, model = Bookings):
    column_list = [c.name for c in Bookings.__table__.c ]+ [Bookings.user,Bookings.room]
    name = 'Booking'
    name_plural = 'Bookings'