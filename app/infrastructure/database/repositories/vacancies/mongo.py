from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from infrastructure.database.converters.vacancies.mongo import (
    vacancy_document_to_entity,
    vacancy_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository

from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.interfaces.repository import BaseVacancyRepository


@dataclass
class MongoVacancyRepository(BaseMongoRepository, BaseVacancyRepository):
    collection_name: str = "vacancies"

    async def add(self, vacancy: VacancyEntity) -> VacancyEntity:
        document = vacancy_entity_to_document(vacancy)
        await self.collection.insert_one(document)
        return vacancy

    async def get_by_id(self, vacancy_id: UUID) -> VacancyEntity | None:
        document = await self.collection.find_one({"oid": str(vacancy_id)})
        if not document:
            return None
        return vacancy_document_to_entity(document)

    async def update(self, vacancy: VacancyEntity) -> None:
        document = vacancy_entity_to_document(vacancy)
        await self.collection.update_one(
            {"oid": str(vacancy.oid)},
            {"$set": document},
        )

    async def delete(self, vacancy_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(vacancy_id)})

    def _build_find_query(self, search: str | None = None, category: str | None = None) -> dict:
        query = {}

        if category:
            query["category"] = category

        if search:
            search_query = {
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"requirements": {"$regex": search, "$options": "i"}},
                    {"experience": {"$regex": search, "$options": "i"}},
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
    ) -> AsyncIterable[VacancyEntity]:
        query = self._build_find_query(search, category)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield vacancy_document_to_entity(document)

    async def count_many(self, search: str | None = None, category: str | None = None) -> int:
        query = self._build_find_query(search, category)
        return await self.collection.count_documents(query)
