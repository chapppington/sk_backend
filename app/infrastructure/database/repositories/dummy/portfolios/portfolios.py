from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.interfaces.repository import BasePortfolioRepository


@dataclass
class DummyInMemoryPortfolioRepository(BasePortfolioRepository):
    _saved_portfolios: list[PortfolioEntity] = field(default_factory=list, kw_only=True)

    async def add(self, portfolio: PortfolioEntity) -> PortfolioEntity:
        self._saved_portfolios.append(portfolio)
        return portfolio

    async def get_by_id(self, portfolio_id: UUID) -> PortfolioEntity | None:
        try:
            return next(portfolio for portfolio in self._saved_portfolios if portfolio.oid == portfolio_id)
        except StopIteration:
            return None

    async def get_by_slug(self, slug: str) -> PortfolioEntity | None:
        try:
            return next(portfolio for portfolio in self._saved_portfolios if portfolio.slug.as_generic_type() == slug)
        except StopIteration:
            return None

    async def update(self, portfolio: PortfolioEntity) -> None:
        for i, saved_portfolio in enumerate(self._saved_portfolios):
            if saved_portfolio.oid == portfolio.oid:
                self._saved_portfolios[i] = portfolio
                return
        raise ValueError(f"Portfolio with id {portfolio.oid} not found")

    async def delete(self, portfolio_id: UUID) -> None:
        self._saved_portfolios = [portfolio for portfolio in self._saved_portfolios if portfolio.oid != portfolio_id]

    def _build_find_query(self, search: str | None = None, year: int | None = None) -> list[PortfolioEntity]:
        filtered_portfolios = self._saved_portfolios.copy()

        if year:
            filtered_portfolios = [
                portfolio for portfolio in filtered_portfolios if portfolio.year.as_generic_type() == year
            ]

        if search:
            search_lower = search.lower()
            filtered_portfolios = [
                portfolio
                for portfolio in filtered_portfolios
                if (
                    search_lower in portfolio.name.as_generic_type().lower()
                    or search_lower in portfolio.description.as_generic_type().lower()
                    or search_lower in portfolio.task_title.as_generic_type().lower()
                    or search_lower in portfolio.task_description.as_generic_type().lower()
                    or search_lower in portfolio.solution_title.as_generic_type().lower()
                    or search_lower in portfolio.solution_description.as_generic_type().lower()
                )
            ]

        return filtered_portfolios

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        year: int | None = None,
    ) -> AsyncIterable[PortfolioEntity]:
        filtered_portfolios = self._build_find_query(search, year)

        reverse = sort_order == -1

        if sort_field == "year":
            filtered_portfolios.sort(key=lambda x: x.year.as_generic_type(), reverse=reverse)
        elif sort_field == "created_at":
            filtered_portfolios.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "name":
            filtered_portfolios.sort(key=lambda x: x.name.as_generic_type(), reverse=reverse)
        else:
            filtered_portfolios.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_portfolios = filtered_portfolios[offset : offset + limit]

        for portfolio in paginated_portfolios:
            yield portfolio

    async def count_many(self, search: str | None = None, year: int | None = None) -> int:
        filtered_portfolios = self._build_find_query(search, year)
        return len(filtered_portfolios)
