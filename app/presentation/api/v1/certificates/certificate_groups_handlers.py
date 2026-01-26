from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from application.certificates.commands import (
    CreateCertificateGroupCommand,
    DeleteCertificateGroupCommand,
    UpdateCertificateGroupCommand,
)
from application.certificates.queries import (
    GetCertificateGroupByIdQuery,
    GetCertificateGroupsListQuery,
)
from application.container import init_container
from application.mediator import Mediator
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
from presentation.api.v1.certificates.schemas import (
    CertificateGroupRequestSchema,
    CertificateGroupResponseSchema,
)


router = APIRouter(prefix="/certificate-groups", tags=["certificate-groups"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[CertificateGroupResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[CertificateGroupResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_certificate_groups_list(
    pagination: PaginationIn = Depends(),
    section: str | None = Query(None, description="Фильтр по секции"),
    is_active: bool | None = Query(None, description="Фильтр по активности"),
    search: str | None = Query(None, description="Поиск по тексту"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[CertificateGroupResponseSchema]]:
    """Получение списка групп сертификатов с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetCertificateGroupsListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        section=section,
        is_active=is_active,
    )

    certificate_groups_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[CertificateGroupResponseSchema]](
        data=ListPaginatedResponse[CertificateGroupResponseSchema](
            items=[
                CertificateGroupResponseSchema.from_entity(certificate_group)
                for certificate_group in certificate_groups_list
            ],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{certificate_group_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CertificateGroupResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CertificateGroupResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_certificate_group_by_id(
    certificate_group_id: UUID,
    container=Depends(init_container),
) -> ApiResponse[CertificateGroupResponseSchema]:
    """Получение группы сертификатов по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetCertificateGroupByIdQuery(certificate_group_id=certificate_group_id)
    certificate_group = await mediator.handle_query(query)

    return ApiResponse[CertificateGroupResponseSchema](
        data=CertificateGroupResponseSchema.from_entity(certificate_group),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[CertificateGroupResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[CertificateGroupResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_certificate_group(
    request: CertificateGroupRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[CertificateGroupResponseSchema]:
    """Создание новой группы сертификатов."""
    mediator: Mediator = container.resolve(Mediator)

    certificate_group = request.to_entity()
    command = CreateCertificateGroupCommand(certificate_group=certificate_group)

    certificate_group, *_ = await mediator.handle_command(command)

    return ApiResponse[CertificateGroupResponseSchema](
        data=CertificateGroupResponseSchema.from_entity(certificate_group),
    )


@router.put(
    "/{certificate_group_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CertificateGroupResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CertificateGroupResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_certificate_group(
    certificate_group_id: UUID,
    request: CertificateGroupRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[CertificateGroupResponseSchema]:
    """Обновление группы сертификатов."""
    mediator: Mediator = container.resolve(Mediator)

    certificate_group = request.to_entity()
    command = UpdateCertificateGroupCommand(
        certificate_group_id=certificate_group_id,
        certificate_group=certificate_group,
    )

    certificate_group, *_ = await mediator.handle_command(command)

    return ApiResponse[CertificateGroupResponseSchema](
        data=CertificateGroupResponseSchema.from_entity(certificate_group),
    )


@router.delete(
    "/{certificate_group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_certificate_group(
    certificate_group_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> None:
    """Удаление группы сертификатов."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteCertificateGroupCommand(certificate_group_id=certificate_group_id)
    await mediator.handle_command(command)
