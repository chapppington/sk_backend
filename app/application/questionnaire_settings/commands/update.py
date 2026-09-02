from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.services import QuestionnaireSettingsService


@dataclass(frozen=True)
class UpdateQuestionnaireSettingsCommand(BaseCommand):
    settings_id: UUID
    settings: QuestionnaireSettingsEntity


@dataclass(frozen=True)
class UpdateQuestionnaireSettingsCommandHandler(
    BaseCommandHandler[UpdateQuestionnaireSettingsCommand, QuestionnaireSettingsEntity],
):
    questionnaire_settings_service: QuestionnaireSettingsService

    async def handle(self, command: UpdateQuestionnaireSettingsCommand) -> QuestionnaireSettingsEntity:
        updated = QuestionnaireSettingsEntity(
            oid=command.settings_id,
            slug=command.settings.slug,
            page_name=command.settings.page_name,
            h1=command.settings.h1,
            subtitle=command.settings.subtitle,
            breadcrumb_label=command.settings.breadcrumb_label,
        )
        return await self.questionnaire_settings_service.update(updated)
