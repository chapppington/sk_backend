from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.interfaces.repository import BaseSeoSettingsRepository
from infrastructure.database.converters.seo_settings.mongo import (
    seo_settings_document_to_entity,
    seo_settings_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoSeoSettingsRepository(BaseMongoRepository, BaseSeoSettingsRepository):
    collection_name: str = "seo_settings"

    async def add(self, seo_settings: SeoSettingsEntity) -> SeoSettingsEntity:
        document = seo_settings_entity_to_document(seo_settings)
        await self.collection.insert_one(document)
        return seo_settings

    async def get_by_id(self, seo_settings_id: UUID) -> SeoSettingsEntity | None:
        document = await self.collection.find_one({"oid": str(seo_settings_id)})
        if not document:
            return None
        return seo_settings_document_to_entity(document)

    async def get_by_path(self, page_path: str) -> SeoSettingsEntity | None:
        document = await self.collection.find_one({"page_path": page_path})
        if not document:
            return None
        return seo_settings_document_to_entity(document)

    async def update(self, seo_settings: SeoSettingsEntity) -> None:
        document = seo_settings_entity_to_document(seo_settings)
        await self.collection.update_one(
            {"oid": str(seo_settings.oid)},
            {"$set": document},
        )

    async def delete(self, seo_settings_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(seo_settings_id)})

    def _build_find_query(self, search: str | None = None, is_active: bool | None = None) -> dict:
        query = {}

        if is_active is not None:
            query["is_active"] = is_active

        if search:
            search_query = {
                "$or": [
                    {"page_path": {"$regex": search, "$options": "i"}},
                    {"page_name": {"$regex": search, "$options": "i"}},
                    {"title": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                ],
            }
            query.update(search_query)

        return query

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> AsyncIterable[SeoSettingsEntity]:
        query = self._build_find_query(search, is_active)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield seo_settings_document_to_entity(document)

    async def count_many(
        self,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> int:
        query = self._build_find_query(search, is_active)
        return await self.collection.count_documents(query)
