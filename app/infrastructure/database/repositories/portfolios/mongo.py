from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from infrastructure.database.converters.portfolios.mongo import (
    portfolio_document_to_entity,
    portfolio_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository

from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.interfaces.repository import BasePortfolioRepository


@dataclass
class MongoPortfolioRepository(BaseMongoRepository, BasePortfolioRepository):
    collection_name: str = "portfolio"

    async def add(self, portfolio: PortfolioEntity) -> PortfolioEntity:
        document = portfolio_entity_to_document(portfolio)
        await self.collection.insert_one(document)
        return portfolio

    async def get_by_id(self, portfolio_id: UUID) -> PortfolioEntity | None:
        document = await self.collection.find_one({"oid": str(portfolio_id)})
        if not document:
            return None
        return portfolio_document_to_entity(document)

    async def get_by_slug(self, slug: str) -> PortfolioEntity | None:
        document = await self.collection.find_one({"slug": slug})
        if not document:
            return None
        return portfolio_document_to_entity(document)

    async def update(self, portfolio: PortfolioEntity) -> None:
        document = portfolio_entity_to_document(portfolio)
        await self.collection.update_one(
            {"oid": str(portfolio.oid)},
            {"$set": document},
        )

    async def delete(self, portfolio_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(portfolio_id)})

    def _build_find_query(self, search: str | None = None, year: int | None = None) -> dict:
        query = {}

        if year:
            query["year"] = year

        if search:
            search_query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"task_title": {"$regex": search, "$options": "i"}},
                    {"task_description": {"$regex": search, "$options": "i"}},
                    {"solution_title": {"$regex": search, "$options": "i"}},
                    {"solution_description": {"$regex": search, "$options": "i"}},
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
        year: int | None = None,
    ) -> AsyncIterable[PortfolioEntity]:
        query = self._build_find_query(search, year)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield portfolio_document_to_entity(document)

    async def count_many(self, search: str | None = None, year: int | None = None) -> int:
        query = self._build_find_query(search, year)
        return await self.collection.count_documents(query)
