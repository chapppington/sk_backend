from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class GetPortfolioByIdQuery(BaseQuery):
    portfolio_id: UUID


@dataclass(frozen=True)
class GetPortfolioByIdQueryHandler(
    BaseQueryHandler[GetPortfolioByIdQuery, PortfolioEntity],
):
    portfolio_service: PortfolioService

    async def handle(
        self,
        query: GetPortfolioByIdQuery,
    ) -> PortfolioEntity:
        return await self.portfolio_service.get_by_id(
            portfolio_id=query.portfolio_id,
        )
