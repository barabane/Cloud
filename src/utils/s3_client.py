import os
from contextlib import asynccontextmanager
from uuid import UUID

from aiobotocore.session import AioSession, get_session
from fastapi import UploadFile

from src.config import settings


class S3:
    def __init__(
        self,
        access_key: str = settings.AWS_ACCESS_KEY_ID,
        secret_key: str = settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url: str = settings.AWS_ENDPOINT_URL,
        region: str = settings.AWS_REGION,
        bucket_name: str = settings.AWS_BUCKET_NAME,
    ) -> None:
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
            'region_name': region,
        }
        self.bucket_name: str = bucket_name
        self.session: AioSession = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_file(self, file_id: UUID, file: UploadFile) -> str:
        async with self.get_client() as client:
            extension = os.path.splitext(file.filename)[1]
            await client.put_object(
                Bucket=self.bucket_name, Key=f'{file_id}{extension}', Body=file.file
            )
            return self.get_file_link(f'{file_id}{extension}')

    async def update_file(self, file_id: UUID, new_file: UploadFile) -> str:
        await self.delete_file(str(file_id))
        return await self.upload_file(file_id, new_file)

    async def delete_file(self, file_id: UUID) -> None:
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=str(file_id))

    def get_file_link(self, file_id: str) -> str:
        return f"{self.config['endpoint_url']}{self.bucket_name}/{file_id}"


s3_client = S3()
