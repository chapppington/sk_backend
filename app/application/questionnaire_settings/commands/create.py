from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.services import QuestionnaireSettingsService


@dataclass(frozen=True)
class CreateQuestionnaireSettingsCommand(BaseCommand):
    settings: QuestionnaireSettingsEntity


@dataclass(frozen=True)
class CreateQuestionnaireSettingsCommandHandler(
    BaseCommandHandler[CreateQuestionnaireSettingsCommand, QuestionnaireSettingsEntity],
):
    questionnaire_settings_service: QuestionnaireSettingsService

    async def handle(self, command: CreateQuestionnaireSettingsCommand) -> QuestionnaireSettingsEntity:
        return await self.questionnaire_settings_service.create(command.settings)
