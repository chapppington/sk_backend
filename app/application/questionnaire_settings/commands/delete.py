from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.questionnaire_settings.services import QuestionnaireSettingsService


@dataclass(frozen=True)
class DeleteQuestionnaireSettingsCommand(BaseCommand):
    settings_id: UUID


@dataclass(frozen=True)
class DeleteQuestionnaireSettingsCommandHandler(
    BaseCommandHandler[DeleteQuestionnaireSettingsCommand, None],
):
    questionnaire_settings_service: QuestionnaireSettingsService

    async def handle(self, command: DeleteQuestionnaireSettingsCommand) -> None:
        await self.questionnaire_settings_service.delete(command.settings_id)
