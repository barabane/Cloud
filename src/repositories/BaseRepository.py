import abc
import uuid

from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(abc.ABC):
    model = None

    async def get_by_id(self, entity_id: str, session: AsyncSession):
        return await session.get(self.model, uuid.UUID(entity_id))

    async def add(self, data, session: AsyncSession):
        res = await session.execute(
            insert(self.model).values(**data).returning(self.model)
        )
        return res.scalar()

    async def delete_by_id(self, entity_id: str, session: AsyncSession):
        return await session.execute(
            delete(self.model).where(self.model.id == uuid.UUID(entity_id))
        )


async def get_base_repository() -> BaseRepository:
    return BaseRepository()
