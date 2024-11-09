from datetime import date
from typing import Optional

from sqlalchemy import select, and_, func, insert, delete, update
from fastapi.responses import JSONResponse

from app.bookings.models import Bookings
from app.exceptions import HotelDoesNotExist
from app.hotels.rooms.models import Rooms
from app.hotels.models import Hotels
from app.hotels.schemas import SListString
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                )
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from,
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    Rooms.hotel_id,
                    Hotels.id,  # Hotel.id
                    Hotels.name,
                    Hotels.location,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                    (
                        Rooms.quantity - func.count(booked_rooms.c.room_id)
                    ).label("rooms_left"),
                )
                .select_from(Rooms)
                .join(
                    booked_rooms,
                    booked_rooms.c.room_id == Rooms.id,
                    isouter=True,
                )
                .join(Hotels, Hotels.id == Rooms.hotel_id, isouter=True)
                .group_by(
                    Rooms.hotel_id,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                )
                .having(
                    and_(
                        Hotels.location.contains(location),
                        Rooms.quantity - func.count(booked_rooms.c.room_id),
                    )
                )
            )

            # print(
            #     get_rooms_left.compile(
            #         engine, compile_kwargs={"literal_binds": True}
            #     )
            # )

            rooms_left = await session.execute(get_rooms_left)
            return rooms_left.mappings().all()

    # проверить группировки в find_all

    # написать, что add ретёрнит
    @classmethod
    async def add_hotel(
        cls,
        name: str,
        location: str,
        services: SListString,
        rooms_quantity: int,
        image_id: int,
    ):
        async with async_session_maker() as session:
            add_hotel = (
                insert(Hotels)
                .values(
                    name=name,
                    location=location,
                    services=services.items,
                    rooms_quantity=rooms_quantity,
                    image_id=image_id,
                )
                .returning(Hotels)
            )

            new_hotel = await session.execute(add_hotel)
            await session.commit()
            return new_hotel.scalar()

    # проверять, что такой отель вообще сущетсвует
    @classmethod
    async def delete_hotel(
        cls,
        hotel_id: int,
    ) -> None:

        async with async_session_maker() as session:
            delete_hotel = delete(Hotels).where(Hotels.id == hotel_id)
        await session.execute(delete_hotel)
        await session.commit()

    @classmethod
    async def update_hotel(
        cls,
        hotel_id: int,
        name: str,
        location: str,
        services: SListString,
        rooms_quantity: int,
        image_id: int,
    ) -> None:

        hotel = await cls.find_by_id(hotel_id)
        if hotel:
            async with async_session_maker() as session:
                updated_info = (
                    update(Hotels)
                    .where(Hotels.id == hotel_id)
                    .values(
                        name=name,
                        location=location,
                        services=services.items,
                        rooms_quantity=rooms_quantity,
                        image_id=image_id,
                    )
                )

                await session.execute(updated_info)
                await session.commit()
        else:
            raise HotelDoesNotExist

    @classmethod
    async def alternative_update_hotel(
        cls,
        hotel_id: int,
        name: Optional[str] = None,
        location: Optional[str] = None,
        services: Optional[SListString] = None,
        rooms_quantity: Optional[int] = None,
        image_id: Optional[int] = None,
    ) -> JSONResponse:

        async with async_session_maker() as session:
            hotel = await cls.find_by_id(hotel_id)

            if hotel:
                if name is not None:
                    update_name = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(name=name)
                    )
                    await session.execute(update_name)

                if location is not None:
                    update_location = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(location=location)
                    )
                    await session.execute(update_location)

                if services is not None:
                    update_services = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(services=services.items)
                    )
                    await session.execute(update_services)

                if rooms_quantity is not None:
                    update_rooms_quantity = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(rooms_quantity=rooms_quantity)
                    )
                    await session.execute(update_rooms_quantity)

                if image_id is not None:
                    update_image_id = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(image_id=image_id)
                    )
                    await session.execute(update_image_id)

                await session.commit()
                return JSONResponse(
                    status_code=200,
                    content={
                        "status_code": 200,
                        "message": "success",
                    },
                )

            else:
                raise HotelDoesNotExist


# не возвращается message, если изменения проходят успешно
# message должен возврашать не дао, а роутер
# перемести эту логику туда
# поменять роутер на патч
