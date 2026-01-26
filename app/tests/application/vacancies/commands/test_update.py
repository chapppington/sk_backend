from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.vacancies.commands import (
    CreateVacancyCommand,
    UpdateVacancyCommand,
)
from application.vacancies.queries import GetVacancyByIdQuery
from domain.vacancies.entities import VacancyEntity
from domain.vacancies.exceptions.vacancies import VacancyNotFoundException
from domain.vacancies.value_objects.vacancies import TitleValueObject


@pytest.mark.asyncio
async def test_update_vacancy_command_success(mediator: Mediator, valid_vacancy_entity: VacancyEntity):
    create_command = CreateVacancyCommand(vacancy=valid_vacancy_entity)
    create_result, *_ = await mediator.handle_command(create_command)
    created_vacancy: VacancyEntity = create_result

    updated_vacancy = VacancyEntity(
        title=TitleValueObject(value="Updated Title"),
        requirements=created_vacancy.requirements,
        experience=created_vacancy.experience,
        salary=created_vacancy.salary,
        category=created_vacancy.category,
    )

    update_command = UpdateVacancyCommand(vacancy_id=created_vacancy.oid, vacancy=updated_vacancy)
    update_result, *_ = await mediator.handle_command(update_command)

    updated: VacancyEntity = update_result

    assert updated.oid == created_vacancy.oid
    assert updated.title.as_generic_type() == "Updated Title"
    assert updated.category.as_generic_type() == created_vacancy.category.as_generic_type()

    retrieved_vacancy = await mediator.handle_query(
        GetVacancyByIdQuery(vacancy_id=created_vacancy.oid),
    )

    assert retrieved_vacancy.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_vacancy_command_not_found(
    mediator: Mediator,
    valid_vacancy_entity: VacancyEntity,
):
    non_existent_id = uuid4()
    update_command = UpdateVacancyCommand(vacancy_id=non_existent_id, vacancy=valid_vacancy_entity)

    with pytest.raises(VacancyNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.vacancy_id == non_existent_id
