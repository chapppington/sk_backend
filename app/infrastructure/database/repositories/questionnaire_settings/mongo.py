from dataclasses import dataclass
from uuid import UUID

from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.interfaces.repository import BaseQuestionnaireSettingsRepository
from infrastructure.database.converters.questionnaire_settings.mongo import (
    questionnaire_settings_document_to_entity,
    questionnaire_settings_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoQuestionnaireSettingsRepository(BaseMongoRepository, BaseQuestionnaireSettingsRepository):
    collection_name: str = "questionnaire_settings"

    async def add(self, settings: QuestionnaireSettingsEntity) -> QuestionnaireSettingsEntity:
        document = questionnaire_settings_entity_to_document(settings)
        await self.collection.insert_one(document)
        return settings

    async def get_by_id(self, settings_id: UUID) -> QuestionnaireSettingsEntity | None:
        document = await self.collection.find_one({"oid": str(settings_id)})
        if not document:
            return None
        return questionnaire_settings_document_to_entity(document)

    async def get_by_slug(self, slug: str) -> QuestionnaireSettingsEntity | None:
        document = await self.collection.find_one({"slug": slug})
        if not document:
            return None
        return questionnaire_settings_document_to_entity(document)

    async def update(self, settings: QuestionnaireSettingsEntity) -> None:
        document = questionnaire_settings_entity_to_document(settings)
        await self.collection.update_one(
            {"oid": str(settings.oid)},
            {"$set": document},
        )

    async def delete(self, settings_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(settings_id)})

    async def find_all(self) -> list[QuestionnaireSettingsEntity]:
        cursor = self.collection.find({}).sort("page_name", 1)
        return [questionnaire_settings_document_to_entity(document) async for document in cursor]
