from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from domain.reviews.entities import ReviewEntity
from domain.reviews.interfaces.repository import BaseReviewRepository
from infrastructure.database.converters.reviews.mongo import (
    review_document_to_entity,
    review_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoReviewRepository(BaseMongoRepository, BaseReviewRepository):
    collection_name: str = "reviews"

    def _build_query(self, category: str | None) -> dict:
        if category is None:
            return {}
        return {"category": category}

    async def add(self, review: ReviewEntity) -> ReviewEntity:
        document = review_entity_to_document(review)
        await self.collection.insert_one(document)
        return review

    async def get_by_id(self, review_id: UUID) -> ReviewEntity | None:
        document = await self.collection.find_one({"oid": str(review_id)})
        if not document:
            return None
        return review_document_to_entity(document)

    async def update(self, review: ReviewEntity) -> None:
        document = review_entity_to_document(review)
        await self.collection.update_one(
            {"oid": str(review.oid)},
            {"$set": document},
        )

    async def delete(self, review_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(review_id)})

    async def find_many(
        self,
        category: str | None,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> AsyncIterable[ReviewEntity]:
        query = self._build_query(category)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield review_document_to_entity(document)

    async def count_many(self, category: str | None) -> int:
        query = self._build_query(category)
        return await self.collection.count_documents(query)
