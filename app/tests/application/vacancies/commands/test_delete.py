from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.vacancies.commands import (
    CreateVacancyCommand,
    DeleteVacancyCommand,
)
from application.vacancies.queries import GetVacancyByIdQuery
from domain.vacancies.entities import VacancyEntity
from domain.vacancies.exceptions.vacancies import VacancyNotFoundException


@pytest.mark.asyncio
async def test_delete_vacancy_command_success(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    create_result, *_ = await mediator.handle_command(
        CreateVacancyCommand(**valid_vacancy_data),
    )
    created_vacancy: VacancyEntity = create_result

    await mediator.handle_command(
        DeleteVacancyCommand(vacancy_id=created_vacancy.oid),
    )

    with pytest.raises(VacancyNotFoundException):
        await mediator.handle_query(
            GetVacancyByIdQuery(vacancy_id=created_vacancy.oid),
        )


@pytest.mark.asyncio
async def test_delete_vacancy_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(VacancyNotFoundException) as exc_info:
        await mediator.handle_command(
            DeleteVacancyCommand(vacancy_id=non_existent_id),
        )

    assert exc_info.value.vacancy_id == non_existent_id
