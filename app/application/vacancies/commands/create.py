from dataclasses import dataclass

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
class CreateVacancyCommand(BaseCommand):
    title: str
    requirements: list[str]
    experience: list[str]
    salary: int
    category: str


@dataclass(frozen=True)
class CreateVacancyCommandHandler(
    BaseCommandHandler[CreateVacancyCommand, VacancyEntity],
):
    vacancy_service: VacancyService

    async def handle(self, command: CreateVacancyCommand) -> VacancyEntity:
        vacancy = VacancyEntity(
            title=TitleValueObject(value=command.title),
            requirements=RequirementsValueObject(value=command.requirements),
            experience=ExperienceValueObject(value=command.experience),
            salary=SalaryValueObject(value=command.salary),
            category=CategoryValueObject(value=command.category),
        )

        return await self.vacancy_service.create(vacancy)
