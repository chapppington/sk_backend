from dataclasses import dataclass

from domain.catalog_texts.entities import CatalogTextEntity
from domain.catalog_texts.exceptions import CatalogTextNotFoundException
from domain.catalog_texts.interfaces.repository import BaseCatalogTextRepository
from domain.catalog_texts.value_objects import (
    CatalogCategoryValueObject,
    CatalogTextContentValueObject,
)


@dataclass
class CatalogTextService:
    catalog_text_repository: BaseCatalogTextRepository

    async def get_by_category(self, category: str) -> CatalogTextEntity:
        normalized = CatalogCategoryValueObject(value=category).as_generic_type()
        catalog_text = await self.catalog_text_repository.get_by_category(normalized)
        if not catalog_text:
            raise CatalogTextNotFoundException(category=normalized)
        return catalog_text

    async def find_all(self) -> list[CatalogTextEntity]:
        return await self.catalog_text_repository.find_all()

    async def upsert(self, category: str, content: dict) -> CatalogTextEntity:
        category_vo = CatalogCategoryValueObject(value=category)
        content_vo = CatalogTextContentValueObject(value=content)
        normalized = category_vo.as_generic_type()
        existing = await self.catalog_text_repository.get_by_category(normalized)

        if existing:
            updated = CatalogTextEntity(
                oid=existing.oid,
                created_at=existing.created_at,
                category=category_vo,
                content=content_vo,
            )
            await self.catalog_text_repository.update(updated)
            return updated

        created = CatalogTextEntity(category=category_vo, content=content_vo)
        await self.catalog_text_repository.add(created)
        return created
