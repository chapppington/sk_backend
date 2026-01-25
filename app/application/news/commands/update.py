from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.news.entities.news import NewsEntity
from domain.news.services import NewsService
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


@dataclass(frozen=True)
class UpdateNewsCommand(BaseCommand):
    news_id: UUID
    category: str
    title: str
    slug: str
    content: str
    short_content: str
    image_url: Optional[str]
    alt: Optional[str]
    reading_time: int
    date: datetime


@dataclass(frozen=True)
class UpdateNewsCommandHandler(
    BaseCommandHandler[UpdateNewsCommand, NewsEntity],
):
    news_service: NewsService

    async def handle(self, command: UpdateNewsCommand) -> NewsEntity:
        existing_news = await self.news_service.get_by_id(command.news_id)

        news = NewsEntity(
            oid=existing_news.oid,
            created_at=existing_news.created_at,
            category=CategoryValueObject(value=command.category),
            title=TitleValueObject(value=command.title),
            slug=SlugValueObject(value=command.slug),
            content=ContentValueObject(value=command.content),
            short_content=ShortContentValueObject(value=command.short_content),
            image_url=ImageUrlValueObject(value=command.image_url),
            alt=AltValueObject(value=command.alt),
            reading_time=ReadingTimeValueObject(value=command.reading_time),
            date=command.date,
        )

        return await self.news_service.update(news)
