import pytest

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from application.vacancies.queries import FindManyVacanciesQuery
from domain.vacancies.entities import VacancyEntity


@pytest.mark.asyncio
async def test_find_many_vacancies_query_success(
    mediator: Mediator,
    valid_vacancy_data_with_category,
):
    for _ in range(5):
        data = valid_vacancy_data_with_category("Производство")
        await mediator.handle_command(
            CreateVacancyCommand(**data),
        )

    result = await mediator.handle_query(
        FindManyVacanciesQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    vacancy_list = [vacancy async for vacancy in result]

    assert len(vacancy_list) == 5
    assert all(isinstance(vacancy, VacancyEntity) for vacancy in vacancy_list)


@pytest.mark.asyncio
async def test_find_many_vacancies_query_with_pagination(
    mediator: Mediator,
    valid_vacancy_data_with_category,
):
    for _ in range(5):
        data = valid_vacancy_data_with_category()
        await mediator.handle_command(
            CreateVacancyCommand(**data),
        )

    result = await mediator.handle_query(
        FindManyVacanciesQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    vacancy_list = [vacancy async for vacancy in result]

    assert len(vacancy_list) == 2

    result = await mediator.handle_query(
        FindManyVacanciesQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    vacancy_list = [vacancy async for vacancy in result]

    assert len(vacancy_list) == 2


@pytest.mark.asyncio
async def test_find_many_vacancies_query_with_category_filter(
    mediator: Mediator,
    valid_vacancy_data_with_category,
):
    for _ in range(3):
        data = valid_vacancy_data_with_category("Производство")
        await mediator.handle_command(
            CreateVacancyCommand(**data),
        )

    for _ in range(2):
        data = valid_vacancy_data_with_category("Продажи и маркетинг")
        await mediator.handle_command(
            CreateVacancyCommand(**data),
        )

    result = await mediator.handle_query(
        FindManyVacanciesQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="Производство",
        ),
    )

    vacancy_list = [vacancy async for vacancy in result]

    assert len(vacancy_list) == 3
    assert all(vacancy.category.as_generic_type() == "Производство" for vacancy in vacancy_list)


@pytest.mark.asyncio
async def test_find_many_vacancies_query_with_search(
    mediator: Mediator,
    valid_vacancy_data_with_category,
):
    data1 = valid_vacancy_data_with_category()
    data1["title"] = "Python Developer"
    await mediator.handle_command(
        CreateVacancyCommand(**data1),
    )

    data2 = valid_vacancy_data_with_category()
    data2["title"] = "JavaScript Developer"
    await mediator.handle_command(
        CreateVacancyCommand(**data2),
    )

    result = await mediator.handle_query(
        FindManyVacanciesQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    vacancy_list = [vacancy async for vacancy in result]

    assert len(vacancy_list) == 1
    assert "Python" in vacancy_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_find_many_vacancies_query_with_sorting(
    mediator: Mediator,
    valid_vacancy_data_with_category,
):
    data1 = valid_vacancy_data_with_category()
    data1["title"] = "First Vacancy"
    await mediator.handle_command(
        CreateVacancyCommand(**data1),
    )

    data2 = valid_vacancy_data_with_category()
    data2["title"] = "Second Vacancy"
    await mediator.handle_command(
        CreateVacancyCommand(**data2),
    )

    result = await mediator.handle_query(
        FindManyVacanciesQuery(
            sort_field="title",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    vacancy_list = [vacancy async for vacancy in result]

    assert len(vacancy_list) == 2
    assert vacancy_list[0].title.as_generic_type() < vacancy_list[1].title.as_generic_type()
