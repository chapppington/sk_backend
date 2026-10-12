from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.catalog_texts.entities import CatalogTextEntity
from domain.catalog_texts.services import CatalogTextService


@dataclass(frozen=True)
class GetCatalogTextListQuery(BaseQuery):
    pass


@dataclass(frozen=True)
class GetCatalogTextListQueryHandler(BaseQueryHandler[GetCatalogTextListQuery, list[CatalogTextEntity]]):
    catalog_text_service: CatalogTextService

    async def handle(self, query: GetCatalogTextListQuery) -> list[CatalogTextEntity]:
        return await self.catalog_text_service.find_all()


@dataclass(frozen=True)
class GetCatalogTextByCategoryQuery(BaseQuery):
    category: str


@dataclass(frozen=True)
class GetCatalogTextByCategoryQueryHandler(BaseQueryHandler[GetCatalogTextByCategoryQuery, CatalogTextEntity]):
    catalog_text_service: CatalogTextService

    async def handle(self, query: GetCatalogTextByCategoryQuery) -> CatalogTextEntity:
        return await self.catalog_text_service.get_by_category(query.category)
