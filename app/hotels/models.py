from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str or None] = mapped_column()
    location: Mapped[str or None] = mapped_column()
    services: Mapped[dict] = mapped_column(JSON)
    rooms_quantity: Mapped[int or None] = mapped_column()
    image_id: Mapped[int] = mapped_column()
