from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.services import SeoSettingsService


@dataclass(frozen=True)
class GetSeoSettingsByPathQuery(BaseQuery):
    page_path: str


@dataclass(frozen=True)
class GetSeoSettingsByPathQueryHandler(
    BaseQueryHandler[GetSeoSettingsByPathQuery, SeoSettingsEntity],
):
    seo_settings_service: SeoSettingsService

    async def handle(
        self,
        query: GetSeoSettingsByPathQuery,
    ) -> SeoSettingsEntity:
        return await self.seo_settings_service.get_by_path(
            page_path=query.page_path,
        )
