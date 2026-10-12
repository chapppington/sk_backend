from datetime import datetime
from uuid import UUID

from domain.catalog_texts.entities import CatalogTextEntity
from domain.catalog_texts.value_objects import (
    CatalogCategoryValueObject,
    CatalogTextContentValueObject,
)


def catalog_text_entity_to_document(entity: CatalogTextEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "category": entity.category.as_generic_type(),
        "content": entity.content.as_generic_type(),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def catalog_text_document_to_entity(document: dict) -> CatalogTextEntity:
    return CatalogTextEntity(
        oid=UUID(document["oid"]),
        category=CatalogCategoryValueObject(value=document["category"]),
        content=CatalogTextContentValueObject(value=document["content"]),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
