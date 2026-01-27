from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.submissions.services import SubmissionService


@dataclass(frozen=True)
class DeleteSubmissionCommand(BaseCommand):
    submission_id: UUID


@dataclass(frozen=True)
class DeleteSubmissionCommandHandler(
    BaseCommandHandler[DeleteSubmissionCommand, None],
):
    submission_service: SubmissionService

    async def handle(self, command: DeleteSubmissionCommand) -> None:
        await self.submission_service.delete(command.submission_id)
