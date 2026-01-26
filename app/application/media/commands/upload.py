from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from infrastructure.s3.base import BaseFileStorage


@dataclass(frozen=True)
class UploadFileCommand(BaseCommand):
    file_obj: BytesIO
    original_filename: str
    bucket_name: str


@dataclass(frozen=True)
class UploadFileCommandHandler(
    BaseCommandHandler[UploadFileCommand, str],
):
    file_storage: BaseFileStorage

    async def handle(self, command: UploadFileCommand) -> str:
        file_extension = Path(command.original_filename).suffix
        file_path = f"{uuid4()}{file_extension}"

        await self.file_storage.upload_file(
            file_obj=command.file_obj,
            file_path=file_path,
            bucket_name=command.bucket_name,
        )

        return file_path
