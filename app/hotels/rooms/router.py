from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.exceptions import (
    HotelDoesNotExist,
    RoomCannotBeAdded,
    RoomDoesNotExist,
)
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.schemas import SListString

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(): ...


# подумать, что сделать с роутером
@router.post("/{hotel_id}/add_room")
async def add_room(
    hotel_id: int,
    name: str,
    description: Optional[str],
    price: int,
    services: SListString,
    quantity: int,
    image_id: int,
) -> JSONResponse:

    if await HotelDAO.hotel_exists(hotel_id=hotel_id):
        room = await RoomsDAO.add_room(
            hotel_id=hotel_id,
            name=name,
            description=description,
            price=price,
            services=services.items,
            quantity=quantity,
            image_id=image_id,
        )

        if room:
            return JSONResponse(
                status_code=200,
                content={
                    "status_code": 200,
                    "message": "Комната успешно добавлена",
                },
            )
        raise RoomCannotBeAdded
    raise HotelDoesNotExist


@router.delete("/delete_room/{room_id}")
async def delete_room(
    room_id: int,
) -> JSONResponse:

    if await RoomsDAO.room_exists(room_id=room_id):
        await RoomsDAO.delete_room(room_id=room_id)
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": "Комната успешно удалена",
            },
        )
    raise RoomDoesNotExist


@router.put("/update_room/{room_id}")
async def update_room(
    room_id: int,
    hotel_id: int,
    name: str,
    price: int,
    services: SListString,
    quantity: int,
    image_id: int,
    description: Optional[str] = None,
) -> JSONResponse:

    if await RoomsDAO.update_room(
        room_id=room_id,
        hotel_id=hotel_id,
        name=name,
        price=price,
        services=services,
        quantity=quantity,
        image_id=image_id,
        description=description,
    ):
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": "Информация о комнате успешно обновлена",
            },
        )
    raise RoomDoesNotExist


@router.patch("/update_room_partly/{room_id}")
async def update_room_partly() -> JSONResponse: ...
