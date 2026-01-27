from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from application.media.exceptions import (
    MediaEmptyFileException,
    MediaFileTooLargeException,
    MediaInvalidContentTypeException,
    MediaInvalidExtensionException,
    MediaInvalidFilenameException,
)
from infrastructure.s3.base import BaseFileStorage


MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
    ".doc",
    ".docx",
    ".csv",
    ".xls",
    ".xlsx",
}


@dataclass(frozen=True)
class UploadFileCommand(BaseCommand):
    file_obj: BytesIO
    original_filename: str
    content_type: str | None
    bucket_name: str


@dataclass(frozen=True)
class UploadFileCommandHandler(
    BaseCommandHandler[UploadFileCommand, str],
):
    file_storage: BaseFileStorage

    async def handle(self, command: UploadFileCommand) -> str:
        if not command.original_filename:
            raise MediaInvalidFilenameException()

        file_extension = Path(command.original_filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise MediaInvalidExtensionException(extension=file_extension)

        if command.content_type not in ALLOWED_CONTENT_TYPES:
            raise MediaInvalidContentTypeException(content_type=command.content_type)

        file_size = len(command.file_obj.getbuffer())

        if file_size == 0:
            raise MediaEmptyFileException()

        if file_size > MAX_FILE_SIZE_BYTES:
            raise MediaFileTooLargeException()

        file_path = f"{uuid4()}{file_extension}"

        await self.file_storage.upload_file(
            file_obj=command.file_obj,
            file_path=file_path,
            bucket_name=command.bucket_name,
        )

        return file_path
