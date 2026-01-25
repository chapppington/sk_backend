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
from presentation.api.v1.vacancies.schemas import (
    CreateVacancyRequestSchema,
    UpdateVacancyRequestSchema,
    VacancyResponseSchema,
)

from application.container import init_container
from application.mediator import Mediator
from application.vacancies.commands import (
    CreateVacancyCommand,
    DeleteVacancyCommand,
    UpdateVacancyCommand,
)
from application.vacancies.queries import (
    CountManyVacanciesQuery,
    FindManyVacanciesQuery,
    GetVacancyByIdQuery,
)


router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[ListPaginatedResponse[VacancyResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[VacancyResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_vacancies_list(
    pagination: PaginationIn = Depends(),
    category: str | None = Query(None, description="Фильтр по категории"),
    search: str | None = Query(None, description="Поиск по тексту"),
    sort_field: str = Query("created_at", description="Поле для сортировки"),
    sort_order: int = Query(-1, description="Порядок сортировки: 1 - по возрастанию, -1 - по убыванию"),
    container=Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[VacancyResponseSchema]]:
    """Получение списка вакансий с фильтрацией и пагинацией."""
    mediator: Mediator = container.resolve(Mediator)

    query = FindManyVacanciesQuery(
        sort_field=sort_field,
        sort_order=sort_order,
        offset=pagination.offset,
        limit=pagination.limit,
        search=search,
        category=category,
    )

    vacancies_list = await mediator.handle_query(query)

    count_query = CountManyVacanciesQuery(search=search, category=category)
    total = await mediator.handle_query(count_query)

    return ApiResponse[ListPaginatedResponse[VacancyResponseSchema]](
        data=ListPaginatedResponse[VacancyResponseSchema](
            items=[VacancyResponseSchema.from_entity(vacancy) for vacancy in vacancies_list],
            pagination=PaginationOut(
                limit=pagination.limit,
                offset=pagination.offset,
                total=total,
            ),
        ),
    )


@router.get(
    "/{vacancy_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[VacancyResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[VacancyResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_vacancy_by_id(
    vacancy_id: UUID,
    container=Depends(init_container),
) -> ApiResponse[VacancyResponseSchema]:
    """Получение вакансии по ID."""
    mediator: Mediator = container.resolve(Mediator)

    query = GetVacancyByIdQuery(vacancy_id=vacancy_id)
    vacancy = await mediator.handle_query(query)

    return ApiResponse[VacancyResponseSchema](
        data=VacancyResponseSchema.from_entity(vacancy),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[VacancyResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[VacancyResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_vacancy(
    request: CreateVacancyRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[VacancyResponseSchema]:
    """Создание новой вакансии."""
    mediator: Mediator = container.resolve(Mediator)

    command = CreateVacancyCommand(
        title=request.title,
        requirements=request.requirements,
        experience=request.experience,
        salary=request.salary,
        category=request.category,
    )

    vacancy, *_ = await mediator.handle_command(command)

    return ApiResponse[VacancyResponseSchema](
        data=VacancyResponseSchema.from_entity(vacancy),
    )


@router.put(
    "/{vacancy_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[VacancyResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[VacancyResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_vacancy(
    vacancy_id: UUID,
    request: UpdateVacancyRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> ApiResponse[VacancyResponseSchema]:
    """Обновление вакансии."""
    mediator: Mediator = container.resolve(Mediator)

    command = UpdateVacancyCommand(
        vacancy_id=vacancy_id,
        title=request.title,
        requirements=request.requirements,
        experience=request.experience,
        salary=request.salary,
        category=request.category,
    )

    vacancy, *_ = await mediator.handle_command(command)

    return ApiResponse[VacancyResponseSchema](
        data=VacancyResponseSchema.from_entity(vacancy),
    )


@router.delete(
    "/{vacancy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_vacancy(
    vacancy_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(init_container),
) -> None:
    """Удаление вакансии."""
    mediator: Mediator = container.resolve(Mediator)

    command = DeleteVacancyCommand(vacancy_id=vacancy_id)
    await mediator.handle_command(command)
