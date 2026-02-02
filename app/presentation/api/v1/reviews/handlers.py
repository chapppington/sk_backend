from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from application.container import get_container
from application.mediator import Mediator
from application.reviews.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    UpdateReviewCommand,
)
from application.reviews.queries import (
    GetReviewByIdQuery,
    GetReviewsListQuery,
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
from presentation.api.v1.reviews.schemas import (
    ReviewRequestSchema,
    ReviewResponseSchema,
)


router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[ReviewResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[ReviewResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_reviews_list(
    pagination: PaginationIn = Depends(),
    category: str | None = Query(None, description="Категория: Сотрудники | Клиенты"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(1, description="Порядок: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[ReviewResponseSchema]]:
    mediator: Mediator = container.resolve(Mediator)

    query = GetReviewsListQuery(
        category=category,
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    reviews_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[ReviewResponseSchema]](
        data=ListPaginatedResponse[ReviewResponseSchema](
            items=[ReviewResponseSchema.from_entity(review) for review in reviews_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{review_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ReviewResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ReviewResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_review_by_id(
    review_id: UUID,
    container=Depends(get_container),
) -> ApiResponse[ReviewResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)

    query = GetReviewByIdQuery(review_id=review_id)
    review = await mediator.handle_query(query)

    return ApiResponse[ReviewResponseSchema](
        data=ReviewResponseSchema.from_entity(review),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[ReviewResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[ReviewResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_review(
    request: ReviewRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[ReviewResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)

    review = request.to_entity()
    command = CreateReviewCommand(review=review)

    review, *_ = await mediator.handle_command(command)

    return ApiResponse[ReviewResponseSchema](
        data=ReviewResponseSchema.from_entity(review),
    )


@router.put(
    "/{review_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ReviewResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ReviewResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_review(
    review_id: UUID,
    request: ReviewRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[ReviewResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)

    review = request.to_entity()
    command = UpdateReviewCommand(review_id=review_id, review=review)

    review, *_ = await mediator.handle_command(command)

    return ApiResponse[ReviewResponseSchema](
        data=ReviewResponseSchema.from_entity(review),
    )


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_review(
    review_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteReviewCommand(review_id=review_id)
    await mediator.handle_command(command)
