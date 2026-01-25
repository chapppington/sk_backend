from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
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
from presentation.api.v1.news.schemas import (
    CreateNewsRequestSchema,
    NewsResponseSchema,
    UpdateNewsRequestSchema,
)

from application.container import init_container
from application.mediator import Mediator
from application.news.commands import (
    CreateNewsCommand,
    DeleteNewsCommand,
    UpdateNewsCommand,
)
from application.news.queries import (
    CountManyNewsQuery,
    FindManyNewsQuery,
    GetNewsByIdQuery,
    GetNewsBySlugQuery,
)


router = APIRouter(prefix="/news", tags=["news"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[NewsResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[NewsResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_news_list(
    pagination: PaginationIn = Depends(),
    category: str | None = Query(None, description="Фильтр по категории"),
    search: str | None = Query(None, description="Поиск по тексту"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[NewsResponseSchema]]:
    """Получение списка новостей с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = FindManyNewsQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        category=category,
    )

    news_list = await mediator.handle_query(query)

    count_query = CountManyNewsQuery(search=search, category=category)
    total = await mediator.handle_query(count_query)

    return ApiResponse[ListPaginatedResponse[NewsResponseSchema]](
        data=ListPaginatedResponse[NewsResponseSchema](
            items=[NewsResponseSchema.from_entity(news) for news in news_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{news_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[NewsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[NewsResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_news_by_id(
    news_id: UUID,
    container=Depends(init_container),
) -> ApiResponse[NewsResponseSchema]:
    """Получение новости по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetNewsByIdQuery(news_id=news_id)
    news = await mediator.handle_query(query)

    return ApiResponse[NewsResponseSchema](
        data=NewsResponseSchema.from_entity(news),
    )


@router.get(
    "/slug/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[NewsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[NewsResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_news_by_slug(
    slug: str,
    container=Depends(init_container),
) -> ApiResponse[NewsResponseSchema]:
    """Получение новости по slug."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetNewsBySlugQuery(slug=slug)
    news = await mediator.handle_query(query)

    return ApiResponse[NewsResponseSchema](
        data=NewsResponseSchema.from_entity(news),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[NewsResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[NewsResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_news(
    request: CreateNewsRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[NewsResponseSchema]:
    """Создание новой новости."""
    mediator: Mediator = container.resolve(Mediator)

    command = CreateNewsCommand(
        category=request.category,
        title=request.title,
        slug=request.slug,
        content=request.content,
        short_content=request.short_content,
        image_url=request.image_url,
        alt=request.alt,
        reading_time=request.reading_time,
        date=request.date,
    )

    news, *_ = await mediator.handle_command(command)

    return ApiResponse[NewsResponseSchema](
        data=NewsResponseSchema.from_entity(news),
    )


@router.put(
    "/{news_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[NewsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[NewsResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_news(
    news_id: UUID,
    request: UpdateNewsRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[NewsResponseSchema]:
    """Обновление новости."""
    mediator: Mediator = container.resolve(Mediator)

    command = UpdateNewsCommand(
        news_id=news_id,
        category=request.category,
        title=request.title,
        slug=request.slug,
        content=request.content,
        short_content=request.short_content,
        image_url=request.image_url,
        alt=request.alt,
        reading_time=request.reading_time,
        date=request.date,
    )

    news, *_ = await mediator.handle_command(command)

    return ApiResponse[NewsResponseSchema](
        data=NewsResponseSchema.from_entity(news),
    )


@router.delete(
    "/{news_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_news(
    news_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> None:
    """Удаление новости."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteNewsCommand(news_id=news_id)
    await mediator.handle_command(command)
