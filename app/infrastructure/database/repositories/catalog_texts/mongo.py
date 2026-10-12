from dataclasses import dataclass

from domain.catalog_texts.entities import CatalogTextEntity
from domain.catalog_texts.interfaces.repository import BaseCatalogTextRepository
from infrastructure.database.converters.catalog_texts.mongo import (
    catalog_text_document_to_entity,
    catalog_text_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoCatalogTextRepository(BaseMongoRepository, BaseCatalogTextRepository):
    collection_name: str = "catalog_texts"

    async def add(self, catalog_text: CatalogTextEntity) -> CatalogTextEntity:
        document = catalog_text_entity_to_document(catalog_text)
        await self.collection.insert_one(document)
        return catalog_text

    async def get_by_category(self, category: str) -> CatalogTextEntity | None:
        document = await self.collection.find_one({"category": category})
        if not document:
            return None
        return catalog_text_document_to_entity(document)

    async def update(self, catalog_text: CatalogTextEntity) -> None:
        document = catalog_text_entity_to_document(catalog_text)
        await self.collection.update_one(
            {"oid": str(catalog_text.oid)},
            {"$set": document},
        )

    async def find_all(self) -> list[CatalogTextEntity]:
        cursor = self.collection.find({}).sort("category", 1)
        return [catalog_text_document_to_entity(document) async for document in cursor]
