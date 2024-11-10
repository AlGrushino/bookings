from typing import List, Optional

from sqlalchemy import and_, delete, func, insert, select, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import SListString


# поменять везде проверку существования на функцию класса
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
    async def delete_room(
        cls,
        room_id: int,
    ):
        async with async_session_maker() as session:
            delete_room = delete(Rooms).where(Rooms.id == room_id)
            await session.execute(delete_room)
            await session.commit()

    # стоит ли давать возможность обновлять информацию об отеле?
    # что должна возвращать функция?
    @classmethod
    async def update_room(
        cls,
        room_id: int,
        hotel_id: int,
        name: str,
        description: Optional[str],
        price: int,
        services: SListString,
        quantity: int,
        image_id: int,
    ) -> bool:

        async with async_session_maker() as session:
            if await cls.room_exists(room_id=room_id):
                updated_info = (
                    update(Rooms)
                    .where(Rooms.id == room_id)
                    .values(
                        hotel_id=hotel_id,
                        name=name,
                        description=description,
                        price=price,
                        services=services.items,
                        quantity=quantity,
                        image_id=image_id,
                    )
                )

                await session.execute(updated_info)
                await session.commit()
                return True
            return False

    @classmethod
    async def update_room_partly(): ...

    @classmethod
    async def room_exists(
        cls,
        room_id: int,
    ) -> bool:

        async with async_session_maker() as session:
            check_existance = select(Rooms).where(Rooms.id == room_id)
            exist = await session.execute(check_existance)
            exist = exist.scalar()

            if exist:
                return True
            return False
