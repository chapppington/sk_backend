from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.container import get_container
from application.mediator import Mediator
from application.warehouse_file.commands import UpsertWarehouseFileCommand
from application.warehouse_file.queries import GetWarehouseFileQuery
from presentation.api.dependencies import get_current_user_id
from presentation.api.schemas import (
    ApiResponse,
    ErrorResponseSchema,
)
from presentation.api.v1.warehouse_file.schemas import (
    WarehouseFileRequestSchema,
    WarehouseFileResponseSchema,
)


router = APIRouter(prefix="/warehouse-file", tags=["warehouse-file"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[WarehouseFileResponseSchema | None],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[WarehouseFileResponseSchema | None]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_warehouse_file(
    container=Depends(get_container),
) -> ApiResponse[WarehouseFileResponseSchema | None]:
    mediator: Mediator = container.resolve(Mediator)
    warehouse_file = await mediator.handle_query(GetWarehouseFileQuery())
    if not warehouse_file:
        return ApiResponse[WarehouseFileResponseSchema | None](data=None)
    return ApiResponse[WarehouseFileResponseSchema | None](
        data=WarehouseFileResponseSchema.from_entity(warehouse_file),
    )


@router.put(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[WarehouseFileResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[WarehouseFileResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def upsert_warehouse_file(
    request: WarehouseFileRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[WarehouseFileResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    command = UpsertWarehouseFileCommand(
        file_url=request.file_url,
        file_name=request.file_name,
    )
    updated, *_ = await mediator.handle_command(command)
    return ApiResponse[WarehouseFileResponseSchema](
        data=WarehouseFileResponseSchema.from_entity(updated),
    )
