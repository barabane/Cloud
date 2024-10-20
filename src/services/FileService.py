from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.FileModel import File
from src.database.schemas.FileSchemas import SFileCreate
from src.repositories.FileRepository import get_file_repository
from src.services.BaseService import BaseService


class FileService(BaseService):
    async def upload_file(
        self, file_request: SFileCreate, session: AsyncSession
    ) -> File | None:
        return await self.repository.add(file_request.__dict__, session)


async def get_file_service() -> FileService:
    return FileService(repository=get_file_repository())
