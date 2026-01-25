import pytest

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from application.vacancies.queries import CountManyVacanciesQuery


@pytest.mark.asyncio
async def test_count_many_vacancies_query_success(
    mediator: Mediator,
    valid_vacancy_data_with_category,
):
    for _ in range(3):
        data = valid_vacancy_data_with_category()
        await mediator.handle_command(
            CreateVacancyCommand(**data),
        )

    count = await mediator.handle_query(
        CountManyVacanciesQuery(),
    )

    assert count == 3


@pytest.mark.asyncio
async def test_count_many_vacancies_query_with_category(
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

    count = await mediator.handle_query(
        CountManyVacanciesQuery(category="Производство"),
    )

    assert count == 3


@pytest.mark.asyncio
async def test_count_many_vacancies_query_with_search(
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

    count = await mediator.handle_query(
        CountManyVacanciesQuery(search="Python"),
    )

    assert count == 1
