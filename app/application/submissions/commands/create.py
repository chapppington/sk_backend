from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.services import SubmissionService


@dataclass(frozen=True)
class CreateSubmissionCommand(BaseCommand):
    submission: SubmissionEntity


@dataclass(frozen=True)
class CreateSubmissionCommandHandler(
    BaseCommandHandler[CreateSubmissionCommand, SubmissionEntity],
):
    submission_service: SubmissionService

    async def handle(self, command: CreateSubmissionCommand) -> SubmissionEntity:
        return await self.submission_service.create(command.submission)
