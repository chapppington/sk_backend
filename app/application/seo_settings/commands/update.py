from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.services import SeoSettingsService


@dataclass(frozen=True)
class UpdateSeoSettingsCommand(BaseCommand):
    seo_settings_id: UUID
    seo_settings: SeoSettingsEntity


@dataclass(frozen=True)
class UpdateSeoSettingsCommandHandler(
    BaseCommandHandler[UpdateSeoSettingsCommand, SeoSettingsEntity],
):
    seo_settings_service: SeoSettingsService

    async def handle(self, command: UpdateSeoSettingsCommand) -> SeoSettingsEntity:
        existing_settings = await self.seo_settings_service.get_by_id(command.seo_settings_id)

        updated_settings = SeoSettingsEntity(
            oid=existing_settings.oid,
            created_at=existing_settings.created_at,
            page_path=command.seo_settings.page_path,
            page_name=command.seo_settings.page_name,
            title=command.seo_settings.title,
            description=command.seo_settings.description,
            keywords=command.seo_settings.keywords,
            og_title=command.seo_settings.og_title,
            og_description=command.seo_settings.og_description,
            og_image=command.seo_settings.og_image,
            canonical_url=command.seo_settings.canonical_url,
            is_active=command.seo_settings.is_active,
        )

        return await self.seo_settings_service.update(updated_settings)
