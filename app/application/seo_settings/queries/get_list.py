import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.services import SeoSettingsService


@dataclass(frozen=True)
class GetSeoSettingsListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass(frozen=True)
class GetSeoSettingsListQueryHandler(
    BaseQueryHandler[GetSeoSettingsListQuery, tuple[list[SeoSettingsEntity], int]],
):
    seo_settings_service: SeoSettingsService

    async def handle(
        self,
        query: GetSeoSettingsListQuery,
    ) -> tuple[list[SeoSettingsEntity], int]:
        settings_task = asyncio.create_task(
            self.seo_settings_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                search=query.search,
                is_active=query.is_active,
            ),
        )
        count_task = asyncio.create_task(
            self.seo_settings_service.count_many(
                search=query.search,
                is_active=query.is_active,
            ),
        )

        return await settings_task, await count_task
