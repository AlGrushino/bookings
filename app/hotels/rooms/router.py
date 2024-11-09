from fastapi import APIRouter

router = APIRouter(prefix="/hotels")


@router.get("/{hotel_id}/rooms")
def get_rooms():
    ...
