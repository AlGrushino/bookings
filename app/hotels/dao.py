from datetime import date

from sqlalchemy import select, and_, func, insert, delete

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.hotels.models import Hotels
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

    # в add добавить проверку на то, что отель ещё не существует по адресу
    # написать, что add ретёрнит
    @classmethod
    async def add(
        cls,
        name: str,
        location: str,
        services: str,
        rooms_quantity: int,
        image_id: int,
    ):
        async with async_session_maker() as session:
            add_hotel = (
                insert(Hotels)
                .values(
                    name=name,
                    location=location,
                    services=services,
                    rooms_quantity=rooms_quantity,
                    image_id=image_id,
                )
                .returning(Hotels)
            )

            new_hotel = await session.execute(add_hotel)
            await session.commit()
            return new_hotel.scalar()

    @classmethod
    async def delete_hotel(
        cls,
        hotel_id: int,
    ) -> None:
        async with async_session_maker() as session:
            delete_hotel = delete(Hotels).where(Hotels.c.id == hotel_id)
        await session.execute(delete_hotel)
        await session.commit()
