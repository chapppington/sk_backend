from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from application.container import get_container
from application.mediator import Mediator
from application.members.commands import (
    CreateMemberCommand,
    DeleteMemberCommand,
    PatchMemberOrderCommand,
    UpdateMemberCommand,
)
from application.members.queries import (
    GetMemberByIdQuery,
    GetMemberListQuery,
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
from presentation.api.v1.members.schemas import (
    MemberOrderPatchSchema,
    MemberRequestSchema,
    MemberResponseSchema,
)


router = APIRouter(prefix="/members", tags=["members"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[MemberResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[MemberResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_members_list(
    pagination: PaginationIn = Depends(),
    sort_field: str = Query("order", description="Поле для сортировки"),
    sort_order: int = Query(1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[MemberResponseSchema]]:
    """Получение списка членов команды с пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetMemberListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    members_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[MemberResponseSchema]](
        data=ListPaginatedResponse[MemberResponseSchema](
            items=[MemberResponseSchema.from_entity(member) for member in members_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{member_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[MemberResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[MemberResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_member_by_id(
    member_id: UUID,
    container=Depends(get_container),
) -> ApiResponse[MemberResponseSchema]:
    """Получение члена команды по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetMemberByIdQuery(member_id=member_id)
    member = await mediator.handle_query(query)

    return ApiResponse[MemberResponseSchema](
        data=MemberResponseSchema.from_entity(member),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[MemberResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[MemberResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_member(
    request: MemberRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[MemberResponseSchema]:
    """Создание нового члена команды."""
    mediator: Mediator = container.resolve(Mediator)

    member = request.to_entity()
    command = CreateMemberCommand(member=member)

    member, *_ = await mediator.handle_command(command)

    return ApiResponse[MemberResponseSchema](
        data=MemberResponseSchema.from_entity(member),
    )


@router.put(
    "/{member_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[MemberResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[MemberResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_member(
    member_id: UUID,
    request: MemberRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[MemberResponseSchema]:
    """Обновление члена команды."""
    mediator: Mediator = container.resolve(Mediator)

    member = request.to_entity()
    command = UpdateMemberCommand(member_id=member_id, member=member)

    member, *_ = await mediator.handle_command(command)

    return ApiResponse[MemberResponseSchema](
        data=MemberResponseSchema.from_entity(member),
    )


@router.patch(
    "/{member_id}/order",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[MemberResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[MemberResponseSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def patch_member_order(
    member_id: UUID,
    request: MemberOrderPatchSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[MemberResponseSchema]:
    """Обновление порядка члена команды."""
    mediator: Mediator = container.resolve(Mediator)

    command = PatchMemberOrderCommand(member_id=member_id, order=request.order)
    member, *_ = await mediator.handle_command(command)

    return ApiResponse[MemberResponseSchema](
        data=MemberResponseSchema.from_entity(member),
    )


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_member(
    member_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> None:
    """Удаление члена команды."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteMemberCommand(member_id=member_id)
    await mediator.handle_command(command)
