from app.dao.base import BaseDao
from app.hotels.rooms.models import Rooms


class RoomsDao(BaseDao):
    model = Rooms


