from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3", future=True)

async_session = async_sessionmaker(engine)



class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)  
    
class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)