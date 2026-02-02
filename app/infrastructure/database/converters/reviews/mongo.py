from datetime import datetime
from uuid import UUID

from domain.reviews.entities import ReviewEntity
from domain.reviews.value_objects.reviews import (
    ReviewCategoryValueObject,
    ReviewContentUrlValueObject,
    ReviewImageValueObject,
    ReviewNameValueObject,
    ReviewPositionValueObject,
    ReviewShortTextValueObject,
    ReviewTextValueObject,
)


def review_entity_to_document(entity: ReviewEntity) -> dict:
    document = {
        "oid": str(entity.oid),
        "name": entity.name.as_generic_type(),
        "category": entity.category.as_generic_type(),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }
    if entity.position:
        document["position"] = entity.position.as_generic_type()
    if entity.image:
        document["image"] = entity.image.as_generic_type()
    if entity.text:
        document["text"] = entity.text.as_generic_type()
    if entity.short_text:
        document["short_text"] = entity.short_text.as_generic_type()
    if entity.content_url:
        document["content_url"] = entity.content_url.as_generic_type()
    return document


def review_document_to_entity(document: dict) -> ReviewEntity:
    return ReviewEntity(
        oid=UUID(document["oid"]),
        name=ReviewNameValueObject(value=document["name"]),
        category=ReviewCategoryValueObject(value=document["category"]),
        position=ReviewPositionValueObject(value=document.get("position")),
        image=ReviewImageValueObject(value=document.get("image")),
        text=ReviewTextValueObject(value=document.get("text")),
        short_text=ReviewShortTextValueObject(value=document.get("short_text")),
        content_url=ReviewContentUrlValueObject(value=document.get("content_url")),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
