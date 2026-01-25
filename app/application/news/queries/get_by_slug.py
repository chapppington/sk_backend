from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.news.entities.news import NewsEntity
from domain.news.services import NewsService


@dataclass(frozen=True)
class GetNewsBySlugQuery(BaseQuery):
    slug: str


@dataclass(frozen=True)
class GetNewsBySlugQueryHandler(
    BaseQueryHandler[GetNewsBySlugQuery, NewsEntity],
):
    news_service: NewsService

    async def handle(
        self,
        query: GetNewsBySlugQuery,
    ) -> NewsEntity:
        return await self.news_service.get_by_slug(
            slug=query.slug,
        )
