import pytest
from faker import Faker

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from application.vacancies.queries import GetVacancyListQuery
from domain.vacancies.entities import VacancyEntity
from domain.vacancies.value_objects.vacancies import TitleValueObject


@pytest.mark.asyncio
async def test_get_vacancy_list_query_success(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
):
    for _ in range(5):
        vacancy = valid_vacancy_entity_with_category("Производство")
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    vacancy_list, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(vacancy_list) == 5
    assert total == 5
    assert all(isinstance(vacancy, VacancyEntity) for vacancy in vacancy_list)


@pytest.mark.asyncio
async def test_get_vacancy_list_query_with_pagination(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
):
    for _ in range(5):
        vacancy = valid_vacancy_entity_with_category()
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    vacancy_list, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(vacancy_list) == 2
    assert total == 5

    vacancy_list, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(vacancy_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_vacancy_list_query_with_category_filter(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
):
    for _ in range(3):
        vacancy = valid_vacancy_entity_with_category("Производство")
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    for _ in range(2):
        vacancy = valid_vacancy_entity_with_category("Продажи и маркетинг")
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    vacancy_list, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="Производство",
        ),
    )

    assert len(vacancy_list) == 3
    assert total == 3
    assert all(vacancy.category.as_generic_type() == "Производство" for vacancy in vacancy_list)


@pytest.mark.asyncio
async def test_get_vacancy_list_query_with_search(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
    faker: Faker,
):
    vacancy1 = valid_vacancy_entity_with_category()
    vacancy1 = VacancyEntity(
        title=TitleValueObject(value="Python Developer"),
        requirements=vacancy1.requirements,
        experience=vacancy1.experience,
        salary=vacancy1.salary,
        category=vacancy1.category,
    )
    await mediator.handle_command(
        CreateVacancyCommand(vacancy=vacancy1),
    )

    vacancy2 = valid_vacancy_entity_with_category()
    vacancy2 = VacancyEntity(
        title=TitleValueObject(value="JavaScript Developer"),
        requirements=vacancy2.requirements,
        experience=vacancy2.experience,
        salary=vacancy2.salary,
        category=vacancy2.category,
    )
    await mediator.handle_command(
        CreateVacancyCommand(vacancy=vacancy2),
    )

    vacancy_list, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(vacancy_list) == 1
    assert total == 1
    assert "Python" in vacancy_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_vacancy_list_query_with_sorting(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
):
    vacancy1 = valid_vacancy_entity_with_category()
    vacancy1 = VacancyEntity(
        title=TitleValueObject(value="First Vacancy"),
        requirements=vacancy1.requirements,
        experience=vacancy1.experience,
        salary=vacancy1.salary,
        category=vacancy1.category,
    )
    await mediator.handle_command(
        CreateVacancyCommand(vacancy=vacancy1),
    )

    vacancy2 = valid_vacancy_entity_with_category()
    vacancy2 = VacancyEntity(
        title=TitleValueObject(value="Second Vacancy"),
        requirements=vacancy2.requirements,
        experience=vacancy2.experience,
        salary=vacancy2.salary,
        category=vacancy2.category,
    )
    await mediator.handle_command(
        CreateVacancyCommand(vacancy=vacancy2),
    )

    vacancy_list, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="title",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(vacancy_list) == 2
    assert total == 2
    assert vacancy_list[0].title.as_generic_type() < vacancy_list[1].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_vacancy_list_query_count_only(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
):
    for _ in range(3):
        vacancy = valid_vacancy_entity_with_category()
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    _, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_vacancy_list_query_count_with_category(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
):
    for _ in range(3):
        vacancy = valid_vacancy_entity_with_category("Производство")
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    for _ in range(2):
        vacancy = valid_vacancy_entity_with_category("Продажи и маркетинг")
        await mediator.handle_command(
            CreateVacancyCommand(vacancy=vacancy),
        )

    _, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="Производство",
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_vacancy_list_query_count_with_search(
    mediator: Mediator,
    valid_vacancy_entity_with_category,
    faker: Faker,
):
    vacancy1 = valid_vacancy_entity_with_category()
    vacancy1 = VacancyEntity(
        title=TitleValueObject(value="Python Developer"),
        requirements=vacancy1.requirements,
        experience=vacancy1.experience,
        salary=vacancy1.salary,
        category=vacancy1.category,
    )
    await mediator.handle_command(
        CreateVacancyCommand(vacancy=vacancy1),
    )

    vacancy2 = valid_vacancy_entity_with_category()
    vacancy2 = VacancyEntity(
        title=TitleValueObject(value="JavaScript Developer"),
        requirements=vacancy2.requirements,
        experience=vacancy2.experience,
        salary=vacancy2.salary,
        category=vacancy2.category,
    )
    await mediator.handle_command(
        CreateVacancyCommand(vacancy=vacancy2),
    )

    _, total = await mediator.handle_query(
        GetVacancyListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert total == 1
