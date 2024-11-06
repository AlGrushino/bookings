from datetime import date

from fastapi import APIRouter

from app.hotels.schemas import SHotelsGetAll
from app.hotels.dao import HotelDAO


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> list[SHotelsGetAll]:

    return await HotelDAO.find_all(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )


# добавить сюда обработку ошибок
