from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class FindManyPortfoliosQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    year: Optional[int] = None


@dataclass(frozen=True)
class FindManyPortfoliosQueryHandler(
    BaseQueryHandler[FindManyPortfoliosQuery, list[PortfolioEntity]],
):
    portfolio_service: PortfolioService

    async def handle(
        self,
        query: FindManyPortfoliosQuery,
    ) -> list[PortfolioEntity]:
        portfolios_iterable = self.portfolio_service.find_many(
            sort_field=query.sort_field,
            sort_order=query.sort_order,
            offset=query.offset,
            limit=query.limit,
            search=query.search,
            year=query.year,
        )
        return [portfolio async for portfolio in portfolios_iterable]
