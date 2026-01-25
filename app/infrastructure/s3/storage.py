from dataclasses import dataclass
from io import BytesIO

from infrastructure.s3.base import BaseFileStorage
from infrastructure.s3.client import S3Client


@dataclass
class S3FileStorage(BaseFileStorage):
    s3_client: S3Client

    async def upload_file(self, file_obj: BytesIO, file_path: str, bucket_name: str) -> None:
        await self.s3_client.upload_fileobj(file_obj, file_path, bucket_name)

    async def get_file_url(self, file_path: str, bucket_name: str, expiration: int = 3600) -> str | None:
        return self.s3_client.get_public_url(file_path, bucket_name)
