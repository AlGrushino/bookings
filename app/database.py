import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///" + \
#     os.path.join(basedir, "app.db")

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///app.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URI)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
