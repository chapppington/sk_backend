from dataclasses import dataclass
from datetime import datetime
from typing import Optional

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
class CreateNewsCommand(BaseCommand):
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
class CreateNewsCommandHandler(
    BaseCommandHandler[CreateNewsCommand, NewsEntity],
):
    news_service: NewsService

    async def handle(self, command: CreateNewsCommand) -> NewsEntity:
        news = NewsEntity(
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

        return await self.news_service.create(news)
