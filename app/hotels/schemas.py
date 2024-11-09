from typing import List

from pydantic import BaseModel, ConfigDict


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SHotelsGetAll(SHotels):
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)


class SListString(BaseModel):
    items: List[str]
