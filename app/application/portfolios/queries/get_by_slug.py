from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class GetPortfolioBySlugQuery(BaseQuery):
    slug: str


@dataclass(frozen=True)
class GetPortfolioBySlugQueryHandler(
    BaseQueryHandler[GetPortfolioBySlugQuery, PortfolioEntity],
):
    portfolio_service: PortfolioService

    async def handle(
        self,
        query: GetPortfolioBySlugQuery,
    ) -> PortfolioEntity:
        return await self.portfolio_service.get_by_slug(
            slug=query.slug,
        )
