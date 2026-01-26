from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.news.entities.news import NewsEntity
from domain.news.services import NewsService


@dataclass(frozen=True)
class CreateNewsCommand(BaseCommand):
    news: NewsEntity


@dataclass(frozen=True)
class CreateNewsCommandHandler(
    BaseCommandHandler[CreateNewsCommand, NewsEntity],
):
    news_service: NewsService

    async def handle(self, command: CreateNewsCommand) -> NewsEntity:
        return await self.news_service.create(command.news)
