from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from application.vacancies.queries import GetVacancyByIdQuery
from domain.vacancies.entities import VacancyEntity
from domain.vacancies.exceptions.vacancies import VacancyNotFoundException


@pytest.mark.asyncio
async def test_get_vacancy_by_id_success(
    mediator: Mediator,
    valid_vacancy_entity: VacancyEntity,
):
    create_result, *_ = await mediator.handle_command(
        CreateVacancyCommand(vacancy=valid_vacancy_entity),
    )
    created_vacancy: VacancyEntity = create_result

    retrieved_vacancy = await mediator.handle_query(
        GetVacancyByIdQuery(vacancy_id=created_vacancy.oid),
    )

    assert retrieved_vacancy.oid == created_vacancy.oid
    assert retrieved_vacancy.category.as_generic_type() == valid_vacancy_entity.category.as_generic_type()
    assert retrieved_vacancy.title.as_generic_type() == valid_vacancy_entity.title.as_generic_type()


@pytest.mark.asyncio
async def test_get_vacancy_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(VacancyNotFoundException) as exc_info:
        await mediator.handle_query(
            GetVacancyByIdQuery(vacancy_id=non_existent_id),
        )

    assert exc_info.value.vacancy_id == non_existent_id
