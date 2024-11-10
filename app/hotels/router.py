from datetime import date
from typing import List, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.exceptions import HotelCannotBeAdded, HotelDoesNotExist
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotelsGetAll, SListString

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

# добавить респонзы и аннтоации к каждой функции


@router.get("/{location}")
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> List[SHotelsGetAll]:

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
) -> JSONResponse:

    hotel = await HotelDAO.add_hotel(
        name=name,
        location=location,
        services=services,
        rooms_quantity=rooms_quantity,
        image_id=image_id,
    )

    if hotel:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": "Отель успешно добавлен",
            },
        )
    raise HotelCannotBeAdded


# пользователь должен быть авторизован и админом
# проверить, что отель существует
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


@router.patch("/update_partly/{hotel_id}")
async def update_hotel_partly(
    hotel_id: int,
    name: Optional[str] = None,
    location: Optional[str] = None,
    services: Optional[SListString] = None,
    rooms_quantity: Optional[int] = None,
    image_id: Optional[int] = None,
) -> JSONResponse:

    hotel = await HotelDAO.update_hotel_partly(
        hotel_id=hotel_id,
        name=name,
        location=location,
        services=services,
        rooms_quantity=rooms_quantity,
        image_id=image_id,
    )

    if hotel:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": "Информация об отеле успешно изменена",
            },
        )
    raise HotelDoesNotExist


# пользователь должен быть авторизован и админом
@router.get("/hotel_exists/{hotel_id}")
async def hotel_exists(hotel_id: int) -> JSONResponse:
    exist = await HotelDAO.hotel_exists(hotel_id=hotel_id)

    if exist:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": "Отель существует",
            },
        )

    return JSONResponse(
        status_code=200,
        content={"status_code": 200, "message": "Отель не существует"},
    )
