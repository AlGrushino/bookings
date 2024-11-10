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
    async def update_room_partly(
        cls,
        room_id: int = None,
        hotel_id: int = None,
        name: str = None,
        description: Optional[str] = None,
        price: int = None,
        services: SListString = None,
        quantity: int = None,
        image_id: int = None,
    ) -> bool:
        flag_changes = False

        async with async_session_maker() as session:
            if await cls.room_exists(room_id=room_id):
                if hotel_id:
                    update_hotel_id = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(hotel_id=hotel_id)
                    )
                    await session.execute(update_hotel_id)
                    flag_changes = True

                if name:
                    update_name = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(name=name)
                    )
                    await session.execute(update_name)
                    flag_changes = True

                if description:
                    update_description = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(description=description)
                    )
                    await session.execute(update_description)
                    flag_changes = True

                if price:
                    update_price = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(price=price)
                    )
                    await session.execute(update_price)
                    flag_changes = True

                if services:
                    update_services = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(services=services.items)
                    )
                    await session.execute(update_services)
                    flag_changes = True

                if quantity:
                    update_quantity = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(quantity=quantity)
                    )
                    await session.execute(update_quantity)
                    flag_changes = True

                if image_id:
                    update_image_id = (
                        update(Rooms)
                        .where(Rooms.id == room_id)
                        .values(image_id=image_id)
                    )
                    await session.execute(update_image_id)
                    flag_changes = True

                if flag_changes:
                    await session.commit()
                    return True
        return False

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
