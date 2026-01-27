from fastapi import status

from application.media.exceptions import (
    MediaEmptyFileException,
    MediaException,
    MediaFileTooLargeException,
    MediaInvalidContentTypeException,
    MediaInvalidExtensionException,
    MediaInvalidFilenameException,
)


def map_media_exception_to_status_code(exc: MediaException) -> int:
    if isinstance(exc, MediaFileTooLargeException):
        return status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    if isinstance(
        exc,
        (
            MediaInvalidFilenameException,
            MediaInvalidExtensionException,
            MediaInvalidContentTypeException,
            MediaEmptyFileException,
        ),
    ):
        return status.HTTP_400_BAD_REQUEST
    return status.HTTP_400_BAD_REQUEST
