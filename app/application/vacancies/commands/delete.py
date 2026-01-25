from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.vacancies.services import VacancyService


@dataclass(frozen=True)
class DeleteVacancyCommand(BaseCommand):
    vacancy_id: UUID


@dataclass(frozen=True)
class DeleteVacancyCommandHandler(
    BaseCommandHandler[DeleteVacancyCommand, None],
):
    vacancy_service: VacancyService

    async def handle(self, command: DeleteVacancyCommand) -> None:
        await self.vacancy_service.delete(command.vacancy_id)
