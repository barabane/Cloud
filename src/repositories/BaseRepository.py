import abc
import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import BaseModel


class BaseRepository(abc.ABC):
    model: BaseModel = None

    async def get_by_id(self, entity_id: str, session: AsyncSession):
        return await session.get(self.model, uuid.UUID(entity_id))

    async def delete_by_id(self, entity_id: str, session: AsyncSession):
        return await session.execute(
            delete(self.model).where(self.model.id == uuid.UUID(entity_id))
        )


async def get_base_repository() -> BaseRepository:
    return BaseRepository()
