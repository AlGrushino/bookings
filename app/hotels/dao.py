from datetime import date
from typing import Optional

from sqlalchemy import and_, delete, func, insert, select, update

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import HotelDoesNotExist
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import SListString


# поменять во всех методах проверку отеля на hotel_exists
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

    # проверять, что такой отель вообще сущетсвует, эту проверку лучше делать в роутере
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

    # убрать обработку ошибок в роутер, возвращать скаляр

    @classmethod
    async def update_hotel_partly(
        cls,
        hotel_id: int,
        name: Optional[str] = None,
        location: Optional[str] = None,
        services: Optional[SListString] = None,
        rooms_quantity: Optional[int] = None,
        image_id: Optional[int] = None,
    ) -> Optional[int]:
        flag_changes: int = 0

        async with async_session_maker() as session:
            get_hotel = select(Hotels).where(Hotels.id == hotel_id)
            hotel = await session.execute(get_hotel)
            hotel = hotel.scalar()

            if hotel:
                if name is not None:
                    update_name = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(name=name)
                    )
                    await session.execute(update_name)
                    flag_changes = 1

                if location is not None:
                    update_location = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(location=location)
                    )
                    await session.execute(update_location)
                    flag_changes = 1

                if services is not None:
                    update_services = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(services=services.items)
                    )
                    await session.execute(update_services)
                    flag_changes = 1

                if rooms_quantity is not None:
                    update_rooms_quantity = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(rooms_quantity=rooms_quantity)
                    )
                    await session.execute(update_rooms_quantity)
                    flag_changes = 1

                if image_id is not None:
                    update_image_id = (
                        update(Hotels)
                        .where(Hotels.id == hotel_id)
                        .values(image_id=image_id)
                    )
                    await session.execute(update_image_id)
                    flag_changes = 1

                await session.commit()
                if flag_changes:
                    return hotel

    # подумать, как бы сделать тут всё одним циклом
    # мб стоит записать аргументы просто как **kwargs

    @classmethod
    async def hotel_exists(
        cls,
        hotel_id: int,
    ) -> bool:

        async with async_session_maker() as session:
            check_existance = select(Hotels).where(Hotels.id == hotel_id)
            exist = await session.execute(check_existance)
            exist = exist.scalar()

            if exist:
                return True
            return False
