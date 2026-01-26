from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.seo_settings.entities import SeoSettingsEntity


class BaseSeoSettingsRepository(ABC):
    @abstractmethod
    async def add(self, seo_settings: SeoSettingsEntity) -> SeoSettingsEntity: ...

    @abstractmethod
    async def get_by_id(self, seo_settings_id: UUID) -> SeoSettingsEntity | None: ...

    @abstractmethod
    async def get_by_path(self, page_path: str) -> SeoSettingsEntity | None: ...

    @abstractmethod
    async def update(self, seo_settings: SeoSettingsEntity) -> None: ...

    @abstractmethod
    async def delete(self, seo_settings_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> AsyncIterable[SeoSettingsEntity]: ...

    @abstractmethod
    async def count_many(
        self,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> int: ...
