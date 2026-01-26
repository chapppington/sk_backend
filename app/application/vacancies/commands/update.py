from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.services import VacancyService


@dataclass(frozen=True)
class UpdateVacancyCommand(BaseCommand):
    vacancy_id: UUID
    vacancy: VacancyEntity


@dataclass(frozen=True)
class UpdateVacancyCommandHandler(
    BaseCommandHandler[UpdateVacancyCommand, VacancyEntity],
):
    vacancy_service: VacancyService

    async def handle(self, command: UpdateVacancyCommand) -> VacancyEntity:
        existing_vacancy = await self.vacancy_service.get_by_id(command.vacancy_id)

        updated_vacancy = VacancyEntity(
            oid=existing_vacancy.oid,
            created_at=existing_vacancy.created_at,
            title=command.vacancy.title,
            requirements=command.vacancy.requirements,
            experience=command.vacancy.experience,
            salary=command.vacancy.salary,
            category=command.vacancy.category,
        )

        return await self.vacancy_service.update(updated_vacancy)
