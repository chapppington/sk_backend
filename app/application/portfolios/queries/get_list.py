import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class GetPortfolioListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    year: Optional[int] = None


@dataclass(frozen=True)
class GetPortfolioListQueryHandler(
    BaseQueryHandler[GetPortfolioListQuery, tuple[list[PortfolioEntity], int]],
):
    portfolio_service: PortfolioService

    async def handle(
        self,
        query: GetPortfolioListQuery,
    ) -> tuple[list[PortfolioEntity], int]:
        portfolios_task = asyncio.create_task(
            self.portfolio_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                search=query.search,
                year=query.year,
            ),
        )
        count_task = asyncio.create_task(
            self.portfolio_service.count_many(
                search=query.search,
                year=query.year,
            ),
        )

        return await portfolios_task, await count_task
