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


@pytest.mark.asyncio
async def test_update_vacancy_command_success(
    mediator: Mediator,
    valid_vacancy_data: dict,
):
    create_result, *_ = await mediator.handle_command(
        CreateVacancyCommand(**valid_vacancy_data),
    )
    created_vacancy: VacancyEntity = create_result

    update_data = valid_vacancy_data.copy()
    update_data["vacancy_id"] = created_vacancy.oid
    update_data["title"] = "Updated Title"

    update_result, *_ = await mediator.handle_command(
        UpdateVacancyCommand(**update_data),
    )

    updated_vacancy: VacancyEntity = update_result

    assert updated_vacancy.oid == created_vacancy.oid
    assert updated_vacancy.title.as_generic_type() == "Updated Title"
    assert updated_vacancy.category.as_generic_type() == update_data["category"]

    retrieved_vacancy = await mediator.handle_query(
        GetVacancyByIdQuery(vacancy_id=created_vacancy.oid),
    )

    assert retrieved_vacancy.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_vacancy_command_not_found(mediator: Mediator, valid_vacancy_data: dict):
    update_data = valid_vacancy_data.copy()
    update_data["vacancy_id"] = uuid4()

    with pytest.raises(VacancyNotFoundException) as exc_info:
        await mediator.handle_command(
            UpdateVacancyCommand(**update_data),
        )

    assert exc_info.value.vacancy_id == update_data["vacancy_id"]
