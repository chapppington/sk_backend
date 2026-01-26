import pytest

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from application.vacancies.queries import GetVacancyByIdQuery
from domain.vacancies.entities import VacancyEntity


@pytest.mark.asyncio
async def test_create_vacancy_command_success(
    mediator: Mediator,
    valid_vacancy_entity: VacancyEntity,
):
    command = CreateVacancyCommand(vacancy=valid_vacancy_entity)
    result, *_ = await mediator.handle_command(command)

    vacancy: VacancyEntity = result

    assert vacancy is not None
    assert vacancy.category.as_generic_type() == valid_vacancy_entity.category.as_generic_type()
    assert vacancy.title.as_generic_type() == valid_vacancy_entity.title.as_generic_type()
    assert vacancy.requirements.as_generic_type() == valid_vacancy_entity.requirements.as_generic_type()
    assert vacancy.experience.as_generic_type() == valid_vacancy_entity.experience.as_generic_type()
    assert vacancy.salary.as_generic_type() == valid_vacancy_entity.salary.as_generic_type()
    assert vacancy.oid is not None

    retrieved_vacancy = await mediator.handle_query(
        GetVacancyByIdQuery(vacancy_id=vacancy.oid),
    )

    assert retrieved_vacancy.oid == vacancy.oid
    assert retrieved_vacancy.title.as_generic_type() == valid_vacancy_entity.title.as_generic_type()
