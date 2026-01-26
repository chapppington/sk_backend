from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.certificates.entities.items import ItemEntity


class BaseItemRepository(ABC):
    @abstractmethod
    async def add(self, item: ItemEntity) -> ItemEntity: ...

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> ItemEntity | None: ...

    @abstractmethod
    async def get_by_title(self, title: str, section: str) -> ItemEntity | None: ...

    @abstractmethod
    async def update(self, item: ItemEntity) -> None: ...

    @abstractmethod
    async def delete(self, item_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> AsyncIterable[ItemEntity]: ...

    @abstractmethod
    async def count_many(
        self,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> int: ...
