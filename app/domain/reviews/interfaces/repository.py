from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.reviews.entities import ReviewEntity


class BaseReviewRepository(ABC):
    @abstractmethod
    async def add(self, review: ReviewEntity) -> ReviewEntity: ...

    @abstractmethod
    async def get_by_id(self, review_id: UUID) -> ReviewEntity | None: ...

    @abstractmethod
    async def update(self, review: ReviewEntity) -> None: ...

    @abstractmethod
    async def delete(self, review_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        category: str | None,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> AsyncIterable[ReviewEntity]: ...

    @abstractmethod
    async def count_many(self, category: str | None) -> int: ...
