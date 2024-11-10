from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.hotels.rooms import router as router_rooms
from app.hotels.router import router as router_hotels
from app.users.router import router as router_users

app = FastAPI()


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms.router)  # разобраться, зачем здесь .router


class HotelsSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(seach_args: HotelsSearchArgs = Depends()):
    return seach_args
