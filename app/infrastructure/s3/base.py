from abc import (
    ABC,
    abstractmethod,
)
from io import BytesIO


class BaseFileStorage(ABC):
    @abstractmethod
    async def upload_file(self, file_obj: BytesIO, file_path: str, bucket_name: str) -> None: ...

    @abstractmethod
    async def get_file_url(
        self,
        file_path: str,
        bucket_name: str,
        expiration: int = 3600,
    ) -> str | None: ...
