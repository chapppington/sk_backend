from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from domain.catalog_texts.entities import CatalogTextEntity


class CatalogTextResponseSchema(BaseModel):
    oid: UUID
    category: str
    content: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: CatalogTextEntity) -> "CatalogTextResponseSchema":
        return cls(
            oid=entity.oid,
            category=entity.category.as_generic_type(),
            content=entity.content.as_generic_type(),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class UpsertCatalogTextRequestSchema(BaseModel):
    content: dict[str, Any]
