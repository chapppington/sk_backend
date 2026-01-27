from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.interfaces.repository import BaseSubmissionRepository
from infrastructure.database.converters.submissions.mongo import (
    submission_document_to_entity,
    submission_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoSubmissionRepository(BaseMongoRepository, BaseSubmissionRepository):
    collection_name: str = "submissions"

    async def add(self, submission: SubmissionEntity) -> SubmissionEntity:
        document = submission_entity_to_document(submission)
        await self.collection.insert_one(document)
        return submission

    async def get_by_id(self, submission_id: UUID) -> SubmissionEntity | None:
        document = await self.collection.find_one({"oid": str(submission_id)})
        if not document:
            return None
        return submission_document_to_entity(document)

    async def delete(self, submission_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(submission_id)})

    def _build_find_query(self, form_type: str | None = None) -> dict:
        query = {}

        if form_type:
            query["form_type"] = form_type

        return query

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        form_type: str | None = None,
    ) -> AsyncIterable[SubmissionEntity]:
        query = self._build_find_query(form_type)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield submission_document_to_entity(document)

    async def count_many(self, form_type: str | None = None) -> int:
        query = self._build_find_query(form_type)
        return await self.collection.count_documents(query)
