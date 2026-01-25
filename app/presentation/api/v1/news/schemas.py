from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain.news.entities.news import NewsEntity


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


class CreateNewsRequestSchema(BaseModel):
    category: str
    title: str
    slug: str
    content: str
    short_content: str
    image_url: Optional[str] = None
    alt: Optional[str] = None
    reading_time: int
    date: datetime


class UpdateNewsRequestSchema(BaseModel):
    category: str
    title: str
    slug: str
    content: str
    short_content: str
    image_url: Optional[str] = None
    alt: Optional[str] = None
    reading_time: int
    date: datetime
