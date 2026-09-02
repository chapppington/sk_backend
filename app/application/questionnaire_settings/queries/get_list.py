from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.services import QuestionnaireSettingsService


@dataclass(frozen=True)
class GetQuestionnaireSettingsListQuery(BaseQuery):
    pass


@dataclass(frozen=True)
class GetQuestionnaireSettingsListQueryHandler(
    BaseQueryHandler[GetQuestionnaireSettingsListQuery, list[QuestionnaireSettingsEntity]],
):
    questionnaire_settings_service: QuestionnaireSettingsService

    async def handle(
        self,
        query: GetQuestionnaireSettingsListQuery,
    ) -> list[QuestionnaireSettingsEntity]:
        return await self.questionnaire_settings_service.find_all()


@dataclass(frozen=True)
class GetQuestionnaireSettingsBySlugQuery(BaseQuery):
    slug: str


@dataclass(frozen=True)
class GetQuestionnaireSettingsBySlugQueryHandler(
    BaseQueryHandler[GetQuestionnaireSettingsBySlugQuery, QuestionnaireSettingsEntity],
):
    questionnaire_settings_service: QuestionnaireSettingsService

    async def handle(
        self,
        query: GetQuestionnaireSettingsBySlugQuery,
    ) -> QuestionnaireSettingsEntity:
        return await self.questionnaire_settings_service.get_by_slug(query.slug)
