from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.catalog_texts.commands import UpsertCatalogTextCommand
from application.catalog_texts.queries import (
    GetCatalogTextByCategoryQuery,
    GetCatalogTextListQuery,
)
from application.container import get_container
from application.mediator import Mediator
from presentation.api.dependencies import get_current_user_id
from presentation.api.schemas import (
    ApiResponse,
    ErrorResponseSchema,
)
from presentation.api.v1.catalog_texts.schemas import (
    CatalogTextResponseSchema,
    UpsertCatalogTextRequestSchema,
)


router = APIRouter(prefix="/catalog-texts", tags=["catalog-texts"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[CatalogTextResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[list[CatalogTextResponseSchema]]},
    },
)
async def get_catalog_text_list(
    container=Depends(get_container),
) -> ApiResponse[list[CatalogTextResponseSchema]]:
    mediator: Mediator = container.resolve(Mediator)
    catalog_texts = await mediator.handle_query(GetCatalogTextListQuery())
    return ApiResponse[list[CatalogTextResponseSchema]](
        data=[CatalogTextResponseSchema.from_entity(item) for item in catalog_texts],
    )


@router.get(
    "/category/{category}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CatalogTextResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CatalogTextResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def get_catalog_text_by_category(
    category: str,
    container=Depends(get_container),
) -> ApiResponse[CatalogTextResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    catalog_text = await mediator.handle_query(GetCatalogTextByCategoryQuery(category=category))
    return ApiResponse[CatalogTextResponseSchema](
        data=CatalogTextResponseSchema.from_entity(catalog_text),
    )


@router.put(
    "/category/{category}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CatalogTextResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CatalogTextResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def upsert_catalog_text(
    category: str,
    request: UpsertCatalogTextRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[CatalogTextResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    command = UpsertCatalogTextCommand(category=category, content=request.content)
    saved, *_ = await mediator.handle_command(command)
    return ApiResponse[CatalogTextResponseSchema](
        data=CatalogTextResponseSchema.from_entity(saved),
    )
