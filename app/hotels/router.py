from datetime import date

from fastapi import APIRouter

from app.hotels.schemas import SHotelsGetAll, SListString
from app.hotels.dao import HotelDAO
from app.exceptions import HotelCannotBeAdded


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


# добавить, что пользователь должен быть авторизован и быть админом
# добавить @router.post("/add/{name}")
@router.post("/add")
async def add_hotel(
    name: str,
    location: str,
    services: SListString,
    rooms_quantity: int,
    image_id: int,
) -> None:

    hotel = await HotelDAO.add_hotel(
        name=name,
        location=location,
        services=services,
        rooms_quantity=rooms_quantity,
        image_id=image_id,
    )

    if not hotel:
        raise HotelCannotBeAdded


# пользователь должен быть авторизован и админом
@router.delete("/delete/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
) -> None:

    await HotelDAO.delete_hotel(
        hotel_id=hotel_id,
    )


# пользователь должен быть авторизован и админом
@router.put("/update/{hotel_id}")
async def update_hotel(
    hotel_id: int,
    name: str,
    location: str,
    services: SListString,
    rooms_quantity: int,
    image_id: int,
) -> None:

    await HotelDAO.update_hotel(
        hotel_id=hotel_id,
        name=name,
        location=location,
        services=services,
        rooms_quantity=rooms_quantity,
        image_id=image_id,
    )
