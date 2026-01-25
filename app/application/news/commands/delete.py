from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.news.services import NewsService


@dataclass(frozen=True)
class DeleteNewsCommand(BaseCommand):
    news_id: UUID


@dataclass(frozen=True)
class DeleteNewsCommandHandler(
    BaseCommandHandler[DeleteNewsCommand, None],
):
    news_service: NewsService

    async def handle(self, command: DeleteNewsCommand) -> None:
        await self.news_service.delete(command.news_id)
