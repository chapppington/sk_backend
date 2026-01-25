from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.portfolios.entities import PortfolioEntity


class BasePortfolioRepository(ABC):
    @abstractmethod
    async def add(self, portfolio: PortfolioEntity) -> PortfolioEntity: ...

    @abstractmethod
    async def get_by_id(self, portfolio_id: UUID) -> PortfolioEntity | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> PortfolioEntity | None: ...

    @abstractmethod
    async def update(self, portfolio: PortfolioEntity) -> None: ...

    @abstractmethod
    async def delete(self, portfolio_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        year: int | None = None,
    ) -> AsyncIterable[PortfolioEntity]: ...

    @abstractmethod
    async def count_many(self, search: str | None = None, year: int | None = None) -> int: ...
