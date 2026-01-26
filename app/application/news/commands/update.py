from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.news.entities.news import NewsEntity
from domain.news.services import NewsService


@dataclass(frozen=True)
class UpdateNewsCommand(BaseCommand):
    news_id: UUID
    news: NewsEntity


@dataclass(frozen=True)
class UpdateNewsCommandHandler(
    BaseCommandHandler[UpdateNewsCommand, NewsEntity],
):
    news_service: NewsService

    async def handle(self, command: UpdateNewsCommand) -> NewsEntity:
        existing_news = await self.news_service.get_by_id(command.news_id)

        updated_news = NewsEntity(
            oid=existing_news.oid,
            created_at=existing_news.created_at,
            category=command.news.category,
            title=command.news.title,
            slug=command.news.slug,
            content=command.news.content,
            short_content=command.news.short_content,
            image_url=command.news.image_url,
            alt=command.news.alt,
            reading_time=command.news.reading_time,
            date=command.news.date,
        )

        return await self.news_service.update(updated_news)
