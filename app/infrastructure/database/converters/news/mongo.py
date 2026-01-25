from datetime import datetime
from uuid import UUID

from domain.news.entities.news import NewsEntity
from domain.news.value_objects.news import (
    AltValueObject,
    CategoryValueObject,
    ContentValueObject,
    ImageUrlValueObject,
    ReadingTimeValueObject,
    ShortContentValueObject,
    SlugValueObject,
    TitleValueObject,
)


def news_entity_to_document(entity: NewsEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "category": entity.category.as_generic_type(),
        "title": entity.title.as_generic_type(),
        "slug": entity.slug.as_generic_type(),
        "content": entity.content.as_generic_type(),
        "short_content": entity.short_content.as_generic_type(),
        "image_url": entity.image_url.as_generic_type(),
        "alt": entity.alt.as_generic_type(),
        "reading_time": entity.reading_time.as_generic_type(),
        "date": entity.date.isoformat(),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def news_document_to_entity(document: dict) -> NewsEntity:
    return NewsEntity(
        oid=UUID(document["oid"]),
        category=CategoryValueObject(value=document["category"]),
        title=TitleValueObject(value=document["title"]),
        slug=SlugValueObject(value=document["slug"]),
        content=ContentValueObject(value=document["content"]),
        short_content=ShortContentValueObject(value=document["short_content"]),
        image_url=ImageUrlValueObject(value=document.get("image_url")),
        alt=AltValueObject(value=document.get("alt")),
        reading_time=ReadingTimeValueObject(value=document["reading_time"]),
        date=datetime.fromisoformat(document["date"]),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
