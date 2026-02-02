from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from application.certificates.commands import (
    CreateCertificateCommand,
    DeleteCertificateCommand,
    PatchCertificateOrderCommand,
    UpdateCertificateCommand,
)
from application.certificates.queries import (
    GetCertificateByIdQuery,
    GetCertificatesListQuery,
)
from application.container import get_container
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
    CertificateOrderPatchSchema,
    CertificateRequestSchema,
    CertificateResponseSchema,
)


router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[CertificateResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[CertificateResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_certificates_list(
    pagination: PaginationIn = Depends(),
    certificate_group_id: UUID | None = Query(None, description="Фильтр по группе сертификатов"),
    search: str | None = Query(None, description="Поиск по тексту"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[CertificateResponseSchema]]:
    """Получение списка сертификатов с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetCertificatesListQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        certificate_group_id=certificate_group_id,
    )

    certificates_list, total = await mediator.handle_query(query)

    return ApiResponse[ListPaginatedResponse[CertificateResponseSchema]](
        data=ListPaginatedResponse[CertificateResponseSchema](
            items=[CertificateResponseSchema.from_entity(certificate) for certificate in certificates_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{certificate_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CertificateResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CertificateResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_certificate_by_id(
    certificate_id: UUID,
    container=Depends(get_container),
) -> ApiResponse[CertificateResponseSchema]:
    """Получение сертификата по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetCertificateByIdQuery(certificate_id=certificate_id)
    certificate = await mediator.handle_query(query)

    return ApiResponse[CertificateResponseSchema](
        data=CertificateResponseSchema.from_entity(certificate),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[CertificateResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[CertificateResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_certificate(
    request: CertificateRequestSchema,
    certificate_group_id: UUID = Query(..., description="ID группы сертификатов"),
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[CertificateResponseSchema]:
    """Создание нового сертификата."""
    mediator: Mediator = container.resolve(Mediator)

    certificate = request.to_entity()
    command = CreateCertificateCommand(
        certificate=certificate,
        certificate_group_id=certificate_group_id,
    )

    certificate, *_ = await mediator.handle_command(command)

    return ApiResponse[CertificateResponseSchema](
        data=CertificateResponseSchema.from_entity(certificate),
    )


@router.put(
    "/{certificate_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CertificateResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CertificateResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_certificate(
    certificate_id: UUID,
    request: CertificateRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[CertificateResponseSchema]:
    """Обновление сертификата."""
    mediator: Mediator = container.resolve(Mediator)

    certificate = request.to_entity()
    command = UpdateCertificateCommand(certificate_id=certificate_id, certificate=certificate)

    certificate, *_ = await mediator.handle_command(command)

    return ApiResponse[CertificateResponseSchema](
        data=CertificateResponseSchema.from_entity(certificate),
    )


@router.patch(
    "/{certificate_id}/order",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CertificateResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[CertificateResponseSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def patch_certificate_order(
    certificate_id: UUID,
    request: CertificateOrderPatchSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[CertificateResponseSchema]:
    """Обновление порядка сертификата."""
    mediator: Mediator = container.resolve(Mediator)

    command = PatchCertificateOrderCommand(
        certificate_id=certificate_id,
        order=request.order,
    )
    certificate, *_ = await mediator.handle_command(command)

    return ApiResponse[CertificateResponseSchema](
        data=CertificateResponseSchema.from_entity(certificate),
    )


@router.delete(
    "/{certificate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_certificate(
    certificate_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> None:
    """Удаление сертификата."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteCertificateCommand(certificate_id=certificate_id)
    await mediator.handle_command(command)
