from collections.abc import AsyncIterable
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.news.entities.news import NewsEntity
from domain.news.interfaces.repository import BaseNewsRepository


@dataclass(frozen=True)
class FindManyNewsQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    category: Optional[str] = None


@dataclass(frozen=True)
class FindManyNewsQueryHandler(
    BaseQueryHandler[FindManyNewsQuery, AsyncIterable[NewsEntity]],
):
    news_repository: BaseNewsRepository

    async def handle(
        self,
        query: FindManyNewsQuery,
    ) -> AsyncIterable[NewsEntity]:
        return self.news_repository.find_many(
            sort_field=query.sort_field,
            sort_order=query.sort_order,
            offset=query.offset,
            limit=query.limit,
            search=query.search,
            category=query.category,
        )
