from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.services import VacancyService


@dataclass(frozen=True)
class CreateVacancyCommand(BaseCommand):
    vacancy: VacancyEntity


@dataclass(frozen=True)
class CreateVacancyCommandHandler(
    BaseCommandHandler[CreateVacancyCommand, VacancyEntity],
):
    vacancy_service: VacancyService

    async def handle(self, command: CreateVacancyCommand) -> VacancyEntity:
        return await self.vacancy_service.create(command.vacancy)
