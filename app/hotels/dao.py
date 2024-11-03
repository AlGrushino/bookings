from datetime import date

from sqlalchemy import select, _and, func

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.hotels.models import Hotels
from app.dao.base import BaseDAO
from app.database import async_session_maker


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
                select(Bookings.id)
                .where(
                    _and(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from,
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    Rooms.hotel_id,
                    Hotels.hotel_id,
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
                    booked_rooms.c.room_id == Rooms.room_id,
                    isouter=True,
                )
                .join(Hotels, Hotels.id == Rooms.hotel_id, isouter=True)
                .group_by(
                    Rooms.hotel_id,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                )
                .having(Rooms.quantity - func.count(booked_rooms.c.room_id))
            )

            rooms_left = await session.execute(get_rooms_left)
            return rooms_left.mappings().all()
