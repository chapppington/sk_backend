from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.services import SeoSettingsService


@dataclass(frozen=True)
class GetSeoSettingsByIdQuery(BaseQuery):
    seo_settings_id: UUID


@dataclass(frozen=True)
class GetSeoSettingsByIdQueryHandler(
    BaseQueryHandler[GetSeoSettingsByIdQuery, SeoSettingsEntity],
):
    seo_settings_service: SeoSettingsService

    async def handle(
        self,
        query: GetSeoSettingsByIdQuery,
    ) -> SeoSettingsEntity:
        return await self.seo_settings_service.get_by_id(
            seo_settings_id=query.seo_settings_id,
        )
