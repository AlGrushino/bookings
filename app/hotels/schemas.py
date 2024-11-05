from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: dict
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SHotelsGetAll(SHotels):
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
