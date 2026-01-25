from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.news.entities.news import NewsEntity
from domain.news.services import NewsService


@dataclass(frozen=True)
class GetNewsByIdQuery(BaseQuery):
    news_id: UUID


@dataclass(frozen=True)
class GetNewsByIdQueryHandler(
    BaseQueryHandler[GetNewsByIdQuery, NewsEntity],
):
    news_service: NewsService

    async def handle(
        self,
        query: GetNewsByIdQuery,
    ) -> NewsEntity:
        return await self.news_service.get_by_id(
            news_id=query.news_id,
        )
