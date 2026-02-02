from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from application.container import get_container
from application.mediator import Mediator
from application.products.commands import (
    CreateProductCommand,
    DeleteProductCommand,
    PatchProductOrderCommand,
    UpdateProductCommand,
)
from application.products.queries import (
    GetProductByIdQuery,
    GetProductBySlugQuery,
    GetProductListQuery,
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
from presentation.api.v1.products.schemas import (
    ProductOrderPatchSchema,
    ProductRequestSchema,
    ProductResponseSchema,
)


router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[ProductResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[ProductResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_products_list(
    pagination: PaginationIn = Depends(),
    category: str | None = Query(None, description="Фильтр по категории"),
    search: str | None = Query(None, description="Поиск по тексту"),
    is_shown: bool | None = Query(None, description="Фильтр по видимости"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[ProductResponseSchema]]:
    """Получение списка продуктов с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetProductListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        category=category,
        is_shown=is_shown,
    )

    products_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[ProductResponseSchema]](
        data=ListPaginatedResponse[ProductResponseSchema](
            items=[ProductResponseSchema.from_entity(product) for product in products_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ProductResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ProductResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_product_by_id(
    product_id: UUID,
    container=Depends(get_container),
) -> ApiResponse[ProductResponseSchema]:
    """Получение продукта по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetProductByIdQuery(product_id=product_id)
    product = await mediator.handle_query(query)

    return ApiResponse[ProductResponseSchema](
        data=ProductResponseSchema.from_entity(product),
    )


@router.get(
    "/slug/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ProductResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ProductResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_product_by_slug(
    slug: str,
    container=Depends(get_container),
) -> ApiResponse[ProductResponseSchema]:
    """Получение продукта по slug."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetProductBySlugQuery(slug=slug)
    product = await mediator.handle_query(query)

    return ApiResponse[ProductResponseSchema](
        data=ProductResponseSchema.from_entity(product),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[ProductResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[ProductResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_product(
    request: ProductRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[ProductResponseSchema]:
    """Создание нового продукта."""
    mediator: Mediator = container.resolve(Mediator)

    product = request.to_entity()
    command = CreateProductCommand(product=product)

    product, *_ = await mediator.handle_command(command)

    return ApiResponse[ProductResponseSchema](
        data=ProductResponseSchema.from_entity(product),
    )


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ProductResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ProductResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_product(
    product_id: UUID,
    request: ProductRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[ProductResponseSchema]:
    """Обновление продукта."""
    mediator: Mediator = container.resolve(Mediator)

    product = request.to_entity()
    command = UpdateProductCommand(product_id=product_id, product=product)

    product, *_ = await mediator.handle_command(command)

    return ApiResponse[ProductResponseSchema](
        data=ProductResponseSchema.from_entity(product),
    )


@router.patch(
    "/{product_id}/order",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ProductResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ProductResponseSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def patch_product_order(
    product_id: UUID,
    request: ProductOrderPatchSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[ProductResponseSchema]:
    """Обновление порядка продукта."""
    mediator: Mediator = container.resolve(Mediator)

    command = PatchProductOrderCommand(product_id=product_id, order=request.order)
    product, *_ = await mediator.handle_command(command)

    return ApiResponse[ProductResponseSchema](
        data=ProductResponseSchema.from_entity(product),
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_product(
    product_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> None:
    """Удаление продукта."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteProductCommand(product_id=product_id)
    await mediator.handle_command(command)
