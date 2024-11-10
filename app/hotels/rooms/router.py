from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.exceptions import HotelDoesNotExist, RoomCannotBeAdded
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.schemas import SListString

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}/rooms")
def get_rooms(): ...


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
def delete_room(): ...


@router.put("/update_room/{room_id}")
def update_room() -> JSONResponse: ...


@router.patch("/update_room_partly/{room_id}")
def update_room_partly() -> JSONResponse: ...
