from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.products.entities import ProductEntity


class BaseProductRepository(ABC):
    @abstractmethod
    async def add(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> ProductEntity | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> ProductEntity | None: ...

    @abstractmethod
    async def update(self, product: ProductEntity) -> None: ...

    @abstractmethod
    async def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> AsyncIterable[ProductEntity]: ...

    @abstractmethod
    async def count_many(
        self,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> int: ...
