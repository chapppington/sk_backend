import pytest

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from application.vacancies.queries import GetVacancyByIdQuery
from domain.vacancies.entities import VacancyEntity
from domain.vacancies.exceptions.vacancies import (
    CategoryInvalidException,
    ExperienceEmptyException,
    RequirementsEmptyException,
    SalaryInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)


@pytest.mark.asyncio
async def test_create_vacancy_command_success(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    result, *_ = await mediator.handle_command(
        CreateVacancyCommand(**valid_vacancy_data),
    )

    vacancy: VacancyEntity = result

    assert vacancy is not None
    assert vacancy.category.as_generic_type() == valid_vacancy_data["category"]
    assert vacancy.title.as_generic_type() == valid_vacancy_data["title"]
    assert vacancy.requirements.as_generic_type() == valid_vacancy_data["requirements"]
    assert vacancy.experience.as_generic_type() == valid_vacancy_data["experience"]
    assert vacancy.salary.as_generic_type() == valid_vacancy_data["salary"]
    assert vacancy.oid is not None

    retrieved_vacancy = await mediator.handle_query(
        GetVacancyByIdQuery(vacancy_id=vacancy.oid),
    )

    assert retrieved_vacancy.oid == vacancy.oid
    assert retrieved_vacancy.title.as_generic_type() == valid_vacancy_data["title"]


@pytest.mark.asyncio
async def test_create_vacancy_command_invalid_category(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    valid_vacancy_data["category"] = "InvalidCategory"

    with pytest.raises(CategoryInvalidException) as exc_info:
        await mediator.handle_command(
            CreateVacancyCommand(**valid_vacancy_data),
        )

    assert exc_info.value.category == "InvalidCategory"


@pytest.mark.asyncio
async def test_create_vacancy_command_empty_title(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    valid_vacancy_data["title"] = ""

    with pytest.raises(TitleEmptyException):
        await mediator.handle_command(
            CreateVacancyCommand(**valid_vacancy_data),
        )


@pytest.mark.asyncio
async def test_create_vacancy_command_title_too_long(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    valid_vacancy_data["title"] = "a" * 256

    with pytest.raises(TitleTooLongException) as exc_info:
        await mediator.handle_command(
            CreateVacancyCommand(**valid_vacancy_data),
        )

    assert exc_info.value.title_length == 256
    assert exc_info.value.max_length == 255


@pytest.mark.asyncio
async def test_create_vacancy_command_empty_requirements(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    valid_vacancy_data["requirements"] = []

    with pytest.raises(RequirementsEmptyException):
        await mediator.handle_command(
            CreateVacancyCommand(**valid_vacancy_data),
        )


@pytest.mark.asyncio
async def test_create_vacancy_command_empty_experience(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    valid_vacancy_data["experience"] = []

    with pytest.raises(ExperienceEmptyException):
        await mediator.handle_command(
            CreateVacancyCommand(**valid_vacancy_data),
        )


@pytest.mark.asyncio
async def test_create_vacancy_command_invalid_salary(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    valid_vacancy_data["salary"] = -1

    with pytest.raises(SalaryInvalidException) as exc_info:
        await mediator.handle_command(
            CreateVacancyCommand(**valid_vacancy_data),
        )

    assert exc_info.value.salary == -1
