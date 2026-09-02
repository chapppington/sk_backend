from dataclasses import dataclass
from uuid import UUID

from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.exceptions import (
    QuestionnaireSettingsAlreadyExistsException,
    QuestionnaireSettingsNotFoundException,
)
from domain.questionnaire_settings.interfaces.repository import BaseQuestionnaireSettingsRepository


@dataclass
class QuestionnaireSettingsService:
    questionnaire_settings_repository: BaseQuestionnaireSettingsRepository

    async def create(self, settings: QuestionnaireSettingsEntity) -> QuestionnaireSettingsEntity:
        slug = settings.slug.as_generic_type()
        existing = await self.questionnaire_settings_repository.get_by_slug(slug)
        if existing:
            raise QuestionnaireSettingsAlreadyExistsException(slug=slug)

        await self.questionnaire_settings_repository.add(settings)
        return settings

    async def get_by_id(self, settings_id: UUID) -> QuestionnaireSettingsEntity:
        settings = await self.questionnaire_settings_repository.get_by_id(settings_id)
        if not settings:
            raise QuestionnaireSettingsNotFoundException(questionnaire_settings_id=str(settings_id))
        return settings

    async def get_by_slug(self, slug: str) -> QuestionnaireSettingsEntity:
        settings = await self.questionnaire_settings_repository.get_by_slug(slug)
        if not settings:
            raise QuestionnaireSettingsNotFoundException(slug=slug)
        return settings

    async def update(self, settings: QuestionnaireSettingsEntity) -> QuestionnaireSettingsEntity:
        existing = await self.questionnaire_settings_repository.get_by_id(settings.oid)
        if not existing:
            raise QuestionnaireSettingsNotFoundException(questionnaire_settings_id=str(settings.oid))

        new_slug = settings.slug.as_generic_type()
        current_slug = existing.slug.as_generic_type()
        if new_slug != current_slug:
            slug_taken = await self.questionnaire_settings_repository.get_by_slug(new_slug)
            if slug_taken:
                raise QuestionnaireSettingsAlreadyExistsException(slug=new_slug)

        updated = QuestionnaireSettingsEntity(
            oid=existing.oid,
            created_at=existing.created_at,
            slug=settings.slug,
            page_name=settings.page_name,
            h1=settings.h1,
            subtitle=settings.subtitle,
            breadcrumb_label=settings.breadcrumb_label,
        )
        await self.questionnaire_settings_repository.update(updated)
        return updated

    async def delete(self, settings_id: UUID) -> None:
        await self.get_by_id(settings_id)
        await self.questionnaire_settings_repository.delete(settings_id)

    async def find_all(self) -> list[QuestionnaireSettingsEntity]:
        return await self.questionnaire_settings_repository.find_all()
