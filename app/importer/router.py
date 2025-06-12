from fastapi import APIRouter, UploadFile, File

from app.hotels.dao import HotelDao
from app.hotels.rooms.dao import RoomsDao
from app.hotels.rooms.schemas import SNewRooms
from app.hotels.schemas import SNewHotels
from app.importer.dependencies import upload_file

router = APIRouter(
    prefix="/importer",
    tags=["importer"]
)


@router.post('/{table_name}', status_code=201)
async def import_csvfile(table_name: str, file: UploadFile = File(...)):
    data = await upload_file(file)

    try:
        for key in data.keys():
            match table_name:
                case 'hotels':
                    new_hotels = SNewHotels(**data[key])
                    await HotelDao.add(**new_hotels.model_dump())
                case 'rooms':
                    new_rooms= SNewRooms(**data[key])
                    await RoomsDao.add(**new_rooms.model_dump())
                case _:
                    raise ValueError(f"Unknown table name: {table_name}")
    except Exception as e:
        print(e)
