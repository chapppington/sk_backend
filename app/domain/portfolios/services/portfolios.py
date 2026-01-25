from dataclasses import dataclass
from uuid import UUID

from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.exceptions import (
    PortfolioAlreadyExistsException,
    PortfolioNotFoundBySlugException,
    PortfolioNotFoundException,
)
from domain.portfolios.interfaces.repository import BasePortfolioRepository


@dataclass
class PortfolioService:
    portfolio_repository: BasePortfolioRepository

    async def create(
        self,
        portfolio: PortfolioEntity,
    ) -> PortfolioEntity:
        existing_portfolio = await self.portfolio_repository.get_by_slug(portfolio.slug.value)

        if existing_portfolio:
            raise PortfolioAlreadyExistsException(slug=portfolio.slug.value)

        await self.portfolio_repository.add(portfolio)

        return portfolio

    async def get_by_id(
        self,
        portfolio_id: UUID,
    ) -> PortfolioEntity:
        portfolio = await self.portfolio_repository.get_by_id(portfolio_id)

        if not portfolio:
            raise PortfolioNotFoundException(portfolio_id=portfolio_id)

        return portfolio

    async def get_by_slug(
        self,
        slug: str,
    ) -> PortfolioEntity:
        portfolio = await self.portfolio_repository.get_by_slug(slug)

        if not portfolio:
            raise PortfolioNotFoundBySlugException(slug=slug)

        return portfolio

    async def update(
        self,
        portfolio: PortfolioEntity,
    ) -> PortfolioEntity:
        existing_portfolio = await self.portfolio_repository.get_by_id(portfolio.oid)

        if not existing_portfolio:
            raise PortfolioNotFoundException(portfolio_id=portfolio.oid)

        existing_by_slug = await self.portfolio_repository.get_by_slug(portfolio.slug.value)

        if existing_by_slug and existing_by_slug.oid != portfolio.oid:
            raise PortfolioAlreadyExistsException(slug=portfolio.slug.value)

        await self.portfolio_repository.update(portfolio)

        return portfolio

    async def delete(
        self,
        portfolio_id: UUID,
    ) -> None:
        await self.get_by_id(portfolio_id)
        await self.portfolio_repository.delete(portfolio_id)
