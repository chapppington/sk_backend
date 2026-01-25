from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class CountManyPortfoliosQuery(BaseQuery):
    search: Optional[str] = None
    year: Optional[int] = None


@dataclass(frozen=True)
class CountManyPortfoliosQueryHandler(
    BaseQueryHandler[CountManyPortfoliosQuery, int],
):
    portfolio_service: PortfolioService

    async def handle(
        self,
        query: CountManyPortfoliosQuery,
    ) -> int:
        return await self.portfolio_service.count_many(
            search=query.search,
            year=query.year,
        )
