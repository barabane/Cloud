from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.schemas.FileSchemas import SFileCreate, SFileResponse, SFileUpdate
from src.services.FileService import FileService, get_file_service
from src.utils.s3_client import s3_client

file_router = APIRouter(prefix='/files', tags=['Files'])


@file_router.get('/{user_id}')
async def get_all_user_files(
    user_id: str,
    file_service: FileService = Depends(get_file_service),
    session: AsyncSession = Depends(get_async_session),
) -> List[SFileResponse]:
    user_files = await file_service.get_all_by_filter(
        user_id=UUID(user_id), session=session
    )
    return [SFileResponse(**file.__dict__) for file in user_files]


@file_router.get('/{file_id}')
async def get_file(
    file_id: str,
    file_service: FileService = Depends(get_file_service),
    session: AsyncSession = Depends(get_async_session),
) -> SFileResponse:
    file = await file_service.get_by_id(file_id, session)
    return SFileResponse(**file)


@file_router.post('/')
async def upload_file(
    user_id,
    file: UploadFile,
    file_service: FileService = Depends(get_file_service),
    session: AsyncSession = Depends(get_async_session),
) -> str:
    file_create = SFileCreate(name=file.filename, size=file.size, user_id=user_id)
    file_model: SFileResponse = await file_service.upload_file(file_create, session)

    file_link: str = await s3_client.upload_file(file_model.id, file)

    return file_link


@file_router.delete('/{file_id}')
async def delete_file(
    file_id: str,
    file_service: FileService = Depends(get_file_service),
    session: AsyncSession = Depends(get_async_session),
):
    await file_service.delete_by_id(file_id.split('.')[0], session)
    await s3_client.delete_file(file_id)

    return True


@file_router.patch('/{file_id}')
async def update_file(
    file_id: str,
    user_id,
    file: UploadFile,
    file_service: FileService = Depends(get_file_service),
    session: AsyncSession = Depends(get_async_session),
):
    file_update = SFileUpdate(name=file.filename, size=file.size, user_id=user_id)
    file_model: SFileResponse = await file_service.update_by_id(
        file_id, file_update.__dict__, session=session
    )

    file_link: str = await s3_client.update_file(file_model.id, file)

    return file_link
