from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.interfaces.repository import BaseSeoSettingsRepository


@dataclass
class DummyInMemorySeoSettingsRepository(BaseSeoSettingsRepository):
    _saved_settings: list[SeoSettingsEntity] = field(default_factory=list, kw_only=True)

    async def add(self, seo_settings: SeoSettingsEntity) -> SeoSettingsEntity:
        self._saved_settings.append(seo_settings)
        return seo_settings

    async def get_by_id(self, seo_settings_id: UUID) -> SeoSettingsEntity | None:
        try:
            return next(settings for settings in self._saved_settings if settings.oid == seo_settings_id)
        except StopIteration:
            return None

    async def get_by_path(self, page_path: str) -> SeoSettingsEntity | None:
        try:
            return next(
                settings for settings in self._saved_settings if settings.page_path.as_generic_type() == page_path
            )
        except StopIteration:
            return None

    async def update(self, seo_settings: SeoSettingsEntity) -> None:
        for i, saved_settings in enumerate(self._saved_settings):
            if saved_settings.oid == seo_settings.oid:
                self._saved_settings[i] = seo_settings
                return
        raise ValueError(f"SEO settings with id {seo_settings.oid} not found")

    async def delete(self, seo_settings_id: UUID) -> None:
        self._saved_settings = [settings for settings in self._saved_settings if settings.oid != seo_settings_id]

    def _build_find_query(
        self,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> list[SeoSettingsEntity]:
        filtered_settings = self._saved_settings.copy()

        if is_active is not None:
            filtered_settings = [settings for settings in filtered_settings if settings.is_active == is_active]

        if search:
            search_lower = search.lower()
            filtered_settings = [
                settings
                for settings in filtered_settings
                if (
                    search_lower in settings.page_path.as_generic_type().lower()
                    or search_lower in settings.page_name.as_generic_type().lower()
                    or search_lower in settings.title.as_generic_type().lower()
                    or search_lower in settings.description.as_generic_type().lower()
                )
            ]

        return filtered_settings

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> AsyncIterable[SeoSettingsEntity]:
        filtered_settings = self._build_find_query(search, is_active)

        reverse = sort_order == -1

        if sort_field == "page_path":
            filtered_settings.sort(key=lambda x: x.page_path.as_generic_type(), reverse=reverse)
        elif sort_field == "page_name":
            filtered_settings.sort(key=lambda x: x.page_name.as_generic_type(), reverse=reverse)
        elif sort_field == "title":
            filtered_settings.sort(key=lambda x: x.title.as_generic_type(), reverse=reverse)
        elif sort_field == "created_at":
            filtered_settings.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "updated_at":
            filtered_settings.sort(key=lambda x: x.updated_at, reverse=reverse)
        else:
            filtered_settings.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_settings = filtered_settings[offset : offset + limit]

        for settings in paginated_settings:
            yield settings

    async def count_many(
        self,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> int:
        filtered_settings = self._build_find_query(search, is_active)
        return len(filtered_settings)
