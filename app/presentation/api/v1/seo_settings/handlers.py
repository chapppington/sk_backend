from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from application.container import init_container
from application.mediator import Mediator
from application.seo_settings.commands import (
    CreateSeoSettingsCommand,
    DeleteSeoSettingsCommand,
    UpdateSeoSettingsCommand,
)
from application.seo_settings.queries import (
    GetSeoSettingsByIdQuery,
    GetSeoSettingsByPathQuery,
    GetSeoSettingsListQuery,
)
from presentation.api.dependencies import get_current_user_id
from presentation.api.filters import (
    PaginationIn,
    PaginationOut,
)
from presentation.api.schemas import (
    ApiResponse,
    ErrorResponseSchema,
    ListPaginatedResponse,
)
from presentation.api.v1.seo_settings.schemas import (
    SeoSettingsRequestSchema,
    SeoSettingsResponseSchema,
)


router = APIRouter(prefix="/seo-settings", tags=["seo-settings"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[SeoSettingsResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[SeoSettingsResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_seo_settings_list(
    pagination: PaginationIn = Depends(),
    search: str | None = Query(None, description="Поиск по тексту"),
    is_active: bool | None = Query(None, description="Фильтр по активности"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[SeoSettingsResponseSchema]]:
    """Получение списка SEO настроек с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetSeoSettingsListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        is_active=is_active,
    )

    settings_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[SeoSettingsResponseSchema]](
        data=ListPaginatedResponse[SeoSettingsResponseSchema](
            items=[SeoSettingsResponseSchema.from_entity(settings) for settings in settings_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{seo_settings_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SeoSettingsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[SeoSettingsResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_seo_settings_by_id(
    seo_settings_id: UUID,
    container=Depends(init_container),
) -> ApiResponse[SeoSettingsResponseSchema]:
    """Получение SEO настроек по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetSeoSettingsByIdQuery(seo_settings_id=seo_settings_id)
    settings = await mediator.handle_query(query)

    return ApiResponse[SeoSettingsResponseSchema](
        data=SeoSettingsResponseSchema.from_entity(settings),
    )


@router.get(
    "/path/{page_path:path}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SeoSettingsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[SeoSettingsResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_seo_settings_by_path(
    page_path: str,
    container=Depends(init_container),
) -> ApiResponse[SeoSettingsResponseSchema]:
    """Получение SEO настроек по пути страницы."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetSeoSettingsByPathQuery(page_path=page_path)
    settings = await mediator.handle_query(query)

    return ApiResponse[SeoSettingsResponseSchema](
        data=SeoSettingsResponseSchema.from_entity(settings),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[SeoSettingsResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[SeoSettingsResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_seo_settings(
    request: SeoSettingsRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[SeoSettingsResponseSchema]:
    """Создание новых SEO настроек."""
    mediator: Mediator = container.resolve(Mediator)

    settings = request.to_entity()
    command = CreateSeoSettingsCommand(seo_settings=settings)

    settings, *_ = await mediator.handle_command(command)

    return ApiResponse[SeoSettingsResponseSchema](
        data=SeoSettingsResponseSchema.from_entity(settings),
    )


@router.put(
    "/{seo_settings_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SeoSettingsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[SeoSettingsResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_seo_settings(
    seo_settings_id: UUID,
    request: SeoSettingsRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[SeoSettingsResponseSchema]:
    """Обновление SEO настроек."""
    mediator: Mediator = container.resolve(Mediator)

    settings = request.to_entity()
    command = UpdateSeoSettingsCommand(seo_settings_id=seo_settings_id, seo_settings=settings)

    settings, *_ = await mediator.handle_command(command)

    return ApiResponse[SeoSettingsResponseSchema](
        data=SeoSettingsResponseSchema.from_entity(settings),
    )


@router.delete(
    "/{seo_settings_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_seo_settings(
    seo_settings_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> None:
    """Удаление SEO настроек."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteSeoSettingsCommand(seo_settings_id=seo_settings_id)
    await mediator.handle_command(command)
