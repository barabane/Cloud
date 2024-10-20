import abc
import uuid

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(abc.ABC):
    model = None

    async def get_by_id(self, entity_id: str, session: AsyncSession):
        return await session.get(self.model, uuid.UUID(entity_id))

    async def get_all(self, session: AsyncSession):
        res = await session.execute(select(self.model))
        return res.scalars().all()

    async def get_all_by_filter(self, session: AsyncSession, **kwargs):
        res = await session.execute(select(self.model).filter_by(**kwargs))
        return res.scalars().all()

    async def add(self, data, session: AsyncSession):
        res = await session.execute(
            insert(self.model).values(**data).returning(self.model)
        )
        return res.scalar()

    async def delete_by_id(self, entity_id: str, session: AsyncSession):
        res = await session.execute(
            delete(self.model)
            .where(self.model.id == uuid.UUID(entity_id))
            .returning(self.model)
        )
        return res.scalar()

    async def update_by_id(self, entity_id: str, data, session: AsyncSession):
        res = await session.execute(
            update(self.model)
            .values(**data)
            .where(self.model.id == uuid.UUID(entity_id))
            .returning(self.model)
        )
        return res.scalar_one_or_none()


async def get_base_repository() -> BaseRepository:
    return BaseRepository()
