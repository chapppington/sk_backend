from io import BytesIO

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    status,
    UploadFile,
)

from application.container import get_container
from application.media.commands import UploadFileCommand
from application.mediator import Mediator
from infrastructure.s3.base import BaseFileStorage
from presentation.api.dependencies import get_current_user_id
from presentation.api.schemas import (
    ApiResponse,
    ErrorResponseSchema,
)
from presentation.api.v1.media.schemas import UploadFileResponseSchema


router = APIRouter(prefix="/media", tags=["media"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[list[UploadFileResponseSchema]],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[list[UploadFileResponseSchema]]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def upload_file(
    files: list[UploadFile] = File(...),
    bucket_name: str = Form(...),
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[list[UploadFileResponseSchema]]:
    """Загрузка файлов в указанный бакет."""
    mediator: Mediator = container.resolve(Mediator)
    file_storage: BaseFileStorage = container.resolve(BaseFileStorage)

    results = []
    for file in files:
        file_content = await file.read()
        file_obj = BytesIO(file_content)

        command = UploadFileCommand(
            file_obj=file_obj,
            original_filename=file.filename or "file",
            content_type=file.content_type,
            bucket_name=bucket_name,
        )

        file_path, *_ = await mediator.handle_command(command)
        file_url = await file_storage.get_file_url(file_path, bucket_name)

        results.append(
            UploadFileResponseSchema(
                file_path=file_path,
                bucket_name=bucket_name,
                file_url=file_url,
            ),
        )

    return ApiResponse[list[UploadFileResponseSchema]](data=results)
