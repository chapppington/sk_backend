from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from domain.news.entities.news import NewsEntity
from domain.news.interfaces.repository import BaseNewsRepository
from infrastructure.database.converters.news.mongo import (
    news_document_to_entity,
    news_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoNewsRepository(BaseMongoRepository, BaseNewsRepository):
    collection_name: str = "news"

    async def add(self, news: NewsEntity) -> NewsEntity:
        document = news_entity_to_document(news)
        await self.collection.insert_one(document)
        return news

    async def get_by_id(self, news_id: UUID) -> NewsEntity | None:
        document = await self.collection.find_one({"oid": str(news_id)})
        if not document:
            return None
        return news_document_to_entity(document)

    async def get_by_slug(self, slug: str) -> NewsEntity | None:
        document = await self.collection.find_one({"slug": slug})
        if not document:
            return None
        return news_document_to_entity(document)

    async def update(self, news: NewsEntity) -> None:
        document = news_entity_to_document(news)
        await self.collection.update_one(
            {"oid": str(news.oid)},
            {"$set": document},
        )

    async def delete(self, news_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(news_id)})

    def _build_find_query(self, search: str | None = None, category: str | None = None) -> dict:
        query = {}

        if category:
            query["category"] = category

        if search:
            search_query = {
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"content": {"$regex": search, "$options": "i"}},
                    {"short_content": {"$regex": search, "$options": "i"}},
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
    ) -> AsyncIterable[NewsEntity]:
        query = self._build_find_query(search, category)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield news_document_to_entity(document)

    async def count_many(self, search: str | None = None, category: str | None = None) -> int:
        query = self._build_find_query(search, category)
        return await self.collection.count_documents(query)
