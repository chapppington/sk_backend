from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from domain.products.entities import ProductEntity
from domain.products.interfaces.repository import BaseProductRepository
from infrastructure.database.converters.products.mongo import (
    product_document_to_entity,
    product_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoProductRepository(BaseMongoRepository, BaseProductRepository):
    collection_name: str = "products"

    async def add(self, product: ProductEntity) -> ProductEntity:
        document = product_entity_to_document(product)
        await self.collection.insert_one(document)
        return product

    async def get_by_id(self, product_id: UUID) -> ProductEntity | None:
        document = await self.collection.find_one({"oid": str(product_id)})
        if not document:
            return None
        return product_document_to_entity(document)

    async def get_by_slug(self, slug: str) -> ProductEntity | None:
        document = await self.collection.find_one({"slug": slug})
        if not document:
            return None
        return product_document_to_entity(document)

    async def update(self, product: ProductEntity) -> None:
        document = product_entity_to_document(product)
        await self.collection.update_one(
            {"oid": str(product.oid)},
            {"$set": document},
        )

    async def delete(self, product_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(product_id)})

    def _build_find_query(
        self,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> dict:
        query = {}

        if category:
            query["category"] = category

        if is_shown is not None:
            query["is_shown"] = is_shown

        if search:
            search_query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"category": {"$regex": search, "$options": "i"}},
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
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> AsyncIterable[ProductEntity]:
        query = self._build_find_query(search, category, is_shown)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield product_document_to_entity(document)

    async def count_many(
        self,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> int:
        query = self._build_find_query(search, category, is_shown)
        return await self.collection.count_documents(query)
