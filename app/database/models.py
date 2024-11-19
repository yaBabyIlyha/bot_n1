from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from dotenv import load_dotenv
import os
load_dotenv()

engine = create_async_engine(url=os.getenv("DATABASE_URL"))
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    how_many: Mapped[str] = mapped_column(String(20)) 
    tg_link: Mapped[str] = mapped_column(String(20))

class Kurs(Base):
    __tablename__ = 'kurs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]

class Notifications(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True)
    on_off: Mapped[int]

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int]

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)