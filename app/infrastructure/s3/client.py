from contextlib import asynccontextmanager

import aioboto3
from botocore.exceptions import ClientError

from settings.config import Config


class S3Client:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.session = aioboto3.Session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.client(
            "s3",
            endpoint_url=self.config.s3_endpoint_url,
            aws_access_key_id=self.config.s3_access_key_id,
            aws_secret_access_key=self.config.s3_secret_access_key,
            use_ssl=self.config.s3_use_ssl,
        ) as client:
            yield client

    async def upload_fileobj(self, file_obj, object_name: str, bucket_name: str) -> None:
        async with self.get_client() as client:
            try:
                await client.head_bucket(Bucket=bucket_name)
            except ClientError as exc:
                error_code = exc.response.get("Error", {}).get("Code", "")
                if error_code in ("404", "NoSuchBucket"):
                    try:
                        await client.create_bucket(Bucket=bucket_name)
                    except ClientError as create_exc:
                        create_code = create_exc.response.get("Error", {}).get("Code", "")
                        if create_code not in ("BucketAlreadyExists", "BucketAlreadyOwnedByYou"):
                            raise
                # 403 и др.: bucket может существовать без прав HeadBucket — пробуем upload
            await client.upload_fileobj(file_obj, bucket_name, object_name)

    def get_public_url(self, object_name: str, bucket_name: str) -> str:
        endpoint = self.config.s3_endpoint_url.rstrip("/")
        return f"{endpoint}/{bucket_name}/{object_name}"
