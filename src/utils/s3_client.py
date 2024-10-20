from contextlib import asynccontextmanager

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

    async def upload_file(self, file_id: str, file: UploadFile) -> str:
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name, Key=str(file_id), Body=file.file
            )
            return self.get_file_link(str(file_id))

    async def delete_file(self, object_name: str) -> None:
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)

    def get_file_link(self, file_id: str) -> str:
        return f"{self.config['endpoint_url']}{self.bucket_name}/{file_id}"


s3_client = S3()
