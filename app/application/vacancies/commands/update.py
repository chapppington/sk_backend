from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.services import VacancyService
from domain.vacancies.value_objects.vacancies import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


@dataclass(frozen=True)
class UpdateVacancyCommand(BaseCommand):
    vacancy_id: UUID
    title: str
    requirements: list[str]
    experience: list[str]
    salary: int
    category: str


@dataclass(frozen=True)
class UpdateVacancyCommandHandler(
    BaseCommandHandler[UpdateVacancyCommand, VacancyEntity],
):
    vacancy_service: VacancyService

    async def handle(self, command: UpdateVacancyCommand) -> VacancyEntity:
        existing_vacancy = await self.vacancy_service.get_by_id(command.vacancy_id)

        vacancy = VacancyEntity(
            oid=existing_vacancy.oid,
            created_at=existing_vacancy.created_at,
            title=TitleValueObject(value=command.title),
            requirements=RequirementsValueObject(value=command.requirements),
            experience=ExperienceValueObject(value=command.experience),
            salary=SalaryValueObject(value=command.salary),
            category=CategoryValueObject(value=command.category),
        )

        return await self.vacancy_service.update(vacancy)
