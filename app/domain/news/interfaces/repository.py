from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.news.entities import NewsEntity


class BaseNewsRepository(ABC):
    @abstractmethod
    async def add(self, news: NewsEntity) -> NewsEntity: ...

    @abstractmethod
    async def get_by_id(self, news_id: UUID) -> NewsEntity | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> NewsEntity | None: ...

    @abstractmethod
    async def update(self, news: NewsEntity) -> None: ...

    @abstractmethod
    async def delete(self, news_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        category: str | None = None,
    ) -> AsyncIterable[NewsEntity]: ...

    @abstractmethod
    async def count_many(self, search: str | None = None, category: str | None = None) -> int: ...
