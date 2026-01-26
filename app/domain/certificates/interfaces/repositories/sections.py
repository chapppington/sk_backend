from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.certificates.entities.sections import SectionEntity


class BaseSectionRepository(ABC):
    @abstractmethod
    async def add(self, section: SectionEntity) -> SectionEntity: ...

    @abstractmethod
    async def get_by_id(self, section_id: UUID) -> SectionEntity | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> SectionEntity | None: ...

    @abstractmethod
    async def update(self, section: SectionEntity) -> None: ...

    @abstractmethod
    async def delete(self, section_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
    ) -> AsyncIterable[SectionEntity]: ...

    @abstractmethod
    async def count_many(
        self,
        search: str | None = None,
    ) -> int: ...
