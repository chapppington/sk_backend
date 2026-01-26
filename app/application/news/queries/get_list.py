import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.news.entities import NewsEntity
from domain.news.services import NewsService


@dataclass(frozen=True)
class GetNewsListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    category: Optional[str] = None


@dataclass(frozen=True)
class GetNewsListQueryHandler(
    BaseQueryHandler[GetNewsListQuery, tuple[list[NewsEntity], int]],
):
    news_service: NewsService

    async def handle(
        self,
        query: GetNewsListQuery,
    ) -> tuple[list[NewsEntity], int]:
        news_task = asyncio.create_task(
            self.news_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                search=query.search,
                category=query.category,
            ),
        )
        count_task = asyncio.create_task(
            self.news_service.count_many(
                search=query.search,
                category=query.category,
            ),
        )

        return await news_task, await count_task
