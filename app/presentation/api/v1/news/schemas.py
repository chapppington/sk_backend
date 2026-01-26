from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

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


class NewsResponseSchema(BaseModel):
    oid: UUID
    category: str
    title: str
    slug: str
    content: str
    short_content: str
    image_url: Optional[str]
    alt: Optional[str]
    reading_time: int
    date: datetime
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: NewsEntity) -> "NewsResponseSchema":
        return cls(
            oid=entity.oid,
            category=entity.category.as_generic_type(),
            title=entity.title.as_generic_type(),
            slug=entity.slug.as_generic_type(),
            content=entity.content.as_generic_type(),
            short_content=entity.short_content.as_generic_type(),
            image_url=entity.image_url.as_generic_type(),
            alt=entity.alt.as_generic_type(),
            reading_time=entity.reading_time.as_generic_type(),
            date=entity.date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class NewsRequestSchema(BaseModel):
    category: str
    title: str
    slug: str
    content: str
    short_content: str
    image_url: Optional[str] = None
    alt: Optional[str] = None
    reading_time: int
    date: datetime

    def to_entity(self) -> NewsEntity:
        return NewsEntity(
            category=CategoryValueObject(value=self.category),
            title=TitleValueObject(value=self.title),
            slug=SlugValueObject(value=self.slug),
            content=ContentValueObject(value=self.content),
            short_content=ShortContentValueObject(value=self.short_content),
            image_url=ImageUrlValueObject(value=self.image_url),
            alt=AltValueObject(value=self.alt),
            reading_time=ReadingTimeValueObject(value=self.reading_time),
            date=self.date,
        )
