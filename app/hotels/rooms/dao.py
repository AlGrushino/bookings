from typing import List, Optional

from sqlalchemy import and_, delete, func, insert, select, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(): ...

    # проверить, что add_room возвращает int
    # проверить количество комнат
    # проверить, что отель существует
    @classmethod
    async def add_room(
        cls,
        hotel_id: int,
        name: str,
        description: Optional[str],
        price: int,
        services: List[str],
        quantity: int,
        image_id: int,
    ) -> int:
        async with async_session_maker() as session:
            add_room = (
                insert(Rooms)
                .values(
                    hotel_id=hotel_id,
                    name=name,
                    description=description,
                    price=price,
                    services=services,
                    quantity=quantity,
                    image_id=image_id,
                )
                .returning(Rooms)
            )

            new_room = await session.execute(add_room)
            await session.commit()
            return new_room.scalar()

    @classmethod
    async def delete_room(): ...

    @classmethod
    async def update_room(): ...

    @classmethod
    async def update_room_partly(): ...
