from uuid import UUID

from fastapi import (
    Depends,
    Query,
    status,
)

from faststream.rabbit.fastapi import RabbitRouter

from application.container import init_container
from application.mediator import Mediator
from application.submissions.commands import (
    CreateSubmissionCommand,
    DeleteSubmissionCommand,
)
from application.submissions.queries import (
    GetSubmissionByIdQuery,
    GetSubmissionListQuery,
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
from presentation.api.v1.submissions.schemas import (
    SubmissionCreatedEventSchema,
    SubmissionRequestSchema,
    SubmissionResponseSchema,
)
from settings.rabbitmq import RabbitMQConfig


# FastStream RabbitMQ Router =================================================

config = RabbitMQConfig()
router = RabbitRouter(
    url=config.rabbitmq_url,
    schema_url=None,
    prefix="/submissions",
    tags=["submissions"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[SubmissionResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[SubmissionResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_submissions_list(
    pagination: PaginationIn = Depends(),
    form_type: str | None = Query(None, description="Фильтр по типу формы"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[SubmissionResponseSchema]]:
    """Получение списка заявок с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetSubmissionListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        form_type=form_type,
    )

    submissions_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[SubmissionResponseSchema]](
        data=ListPaginatedResponse[SubmissionResponseSchema](
            items=[SubmissionResponseSchema.from_entity(submission) for submission in submissions_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SubmissionResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[SubmissionResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_submission_by_id(
    submission_id: UUID,
    container=Depends(init_container),
) -> ApiResponse[SubmissionResponseSchema]:
    """Получение заявки по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetSubmissionByIdQuery(submission_id=submission_id)
    submission = await mediator.handle_query(query)

    return ApiResponse[SubmissionResponseSchema](
        data=SubmissionResponseSchema.from_entity(submission),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[SubmissionResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[SubmissionResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_submission(
    request: SubmissionRequestSchema,
    container=Depends(init_container),
) -> ApiResponse[SubmissionResponseSchema]:
    """Создание новой заявки."""
    mediator: Mediator = container.resolve(Mediator)

    submission = request.to_entity()
    command = CreateSubmissionCommand(submission=submission)

    submission, *_ = await mediator.handle_command(command)

    event = SubmissionCreatedEventSchema.from_entity(submission)

    await router.broker.publish(
        event.model_dump(),
        queue="submission_created",
    )

    return ApiResponse[SubmissionResponseSchema](
        data=SubmissionResponseSchema.from_entity(submission),
    )


@router.delete(
    "/{submission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_submission(
    submission_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> None:
    """Удаление заявки."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteSubmissionCommand(submission_id=submission_id)
    await mediator.handle_command(command)
