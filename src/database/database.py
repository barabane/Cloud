from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


DB_URL = settings.DATABASE_URL

if settings.MODE == 'TEST':
    DB_URL = settings.TEST_DATABASE_URL

engine = create_async_engine(url=str(DB_URL))
async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()
        await session.close()
