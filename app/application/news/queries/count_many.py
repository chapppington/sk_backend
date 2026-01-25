from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.news.interfaces.repository import BaseNewsRepository


@dataclass(frozen=True)
class CountManyNewsQuery(BaseQuery):
    search: Optional[str] = None
    category: Optional[str] = None


@dataclass(frozen=True)
class CountManyNewsQueryHandler(
    BaseQueryHandler[CountManyNewsQuery, int],
):
    news_repository: BaseNewsRepository

    async def handle(
        self,
        query: CountManyNewsQuery,
    ) -> int:
        return await self.news_repository.count_many(
            search=query.search,
            category=query.category,
        )
