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
from presentation.api.v1.portfolios.schemas import (
    PortfolioRequestSchema,
    PortfolioResponseSchema,
)

from application.container import init_container
from application.mediator import Mediator
from application.portfolios.commands import (
    CreatePortfolioCommand,
    DeletePortfolioCommand,
    UpdatePortfolioCommand,
)
from application.portfolios.queries import (
    GetPortfolioByIdQuery,
    GetPortfolioBySlugQuery,
    GetPortfolioListQuery,
)


router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[PortfolioResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[PortfolioResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_portfolios_list(
    pagination: PaginationIn = Depends(),
    year: int | None = Query(None, description="Фильтр по году"),
    search: str | None = Query(None, description="Поиск по тексту"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[PortfolioResponseSchema]]:
    """Получение списка портфолио с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetPortfolioListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        year=year,
    )

    portfolios_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[PortfolioResponseSchema]](
        data=ListPaginatedResponse[PortfolioResponseSchema](
            items=[PortfolioResponseSchema.from_entity(portfolio) for portfolio in portfolios_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PortfolioResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[PortfolioResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_portfolio_by_id(
    portfolio_id: UUID,
    container=Depends(init_container),
) -> ApiResponse[PortfolioResponseSchema]:
    """Получение портфолио по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetPortfolioByIdQuery(portfolio_id=portfolio_id)
    portfolio = await mediator.handle_query(query)

    return ApiResponse[PortfolioResponseSchema](
        data=PortfolioResponseSchema.from_entity(portfolio),
    )


@router.get(
    "/slug/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PortfolioResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[PortfolioResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_portfolio_by_slug(
    slug: str,
    container=Depends(init_container),
) -> ApiResponse[PortfolioResponseSchema]:
    """Получение портфолио по slug."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetPortfolioBySlugQuery(slug=slug)
    portfolio = await mediator.handle_query(query)

    return ApiResponse[PortfolioResponseSchema](
        data=PortfolioResponseSchema.from_entity(portfolio),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[PortfolioResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[PortfolioResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_portfolio(
    request: PortfolioRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[PortfolioResponseSchema]:
    """Создание нового портфолио."""
    mediator: Mediator = container.resolve(Mediator)

    portfolio = request.to_entity()
    command = CreatePortfolioCommand(portfolio=portfolio)

    portfolio, *_ = await mediator.handle_command(command)

    return ApiResponse[PortfolioResponseSchema](
        data=PortfolioResponseSchema.from_entity(portfolio),
    )


@router.put(
    "/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PortfolioResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[PortfolioResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_portfolio(
    portfolio_id: UUID,
    request: PortfolioRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[PortfolioResponseSchema]:
    """Обновление портфолио."""
    mediator: Mediator = container.resolve(Mediator)

    portfolio = request.to_entity()
    command = UpdatePortfolioCommand(portfolio_id=portfolio_id, portfolio=portfolio)

    portfolio, *_ = await mediator.handle_command(command)

    return ApiResponse[PortfolioResponseSchema](
        data=PortfolioResponseSchema.from_entity(portfolio),
    )


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_portfolio(
    portfolio_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> None:
    """Удаление портфолио."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeletePortfolioCommand(portfolio_id=portfolio_id)
    await mediator.handle_command(command)
