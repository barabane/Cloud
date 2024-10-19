from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(url=str(settings.DATABASE_URL))
async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)
