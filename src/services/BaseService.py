import abc

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.BaseRepository import BaseRepository, get_base_repository


class BaseService(abc.ABC):
    def __init__(self, repository: BaseRepository) -> None:
        self.repository: BaseRepository = repository

    async def get_by_id(self, entity_id: str, session: AsyncSession):
        return await self.repository.get_by_id(entity_id=entity_id, session=session)

    async def get_all(self, session: AsyncSession):
        return await self.repository.get_all(session=session)

    async def get_all_by_filter(self, session: AsyncSession, **kwargs):
        return await self.repository.get_all_by_filter(session=session, **kwargs)

    async def add(self, data, session: AsyncSession):
        return await self.repository.add(data, session)

    async def delete_by_id(self, entity_id: str, session: AsyncSession):
        return await self.repository.delete_by_id(entity_id=entity_id, session=session)

    async def update_by_id(self, entity_id: str, data, session: AsyncSession):
        return await self.repository.update_by_id(
            entity_id=entity_id, data=data, session=session
        )


async def get_base_service() -> BaseService:
    return BaseService(repository=get_base_repository())
