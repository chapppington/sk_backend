from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.services import SeoSettingsService


@dataclass(frozen=True)
class CreateSeoSettingsCommand(BaseCommand):
    seo_settings: SeoSettingsEntity


@dataclass(frozen=True)
class CreateSeoSettingsCommandHandler(
    BaseCommandHandler[CreateSeoSettingsCommand, SeoSettingsEntity],
):
    seo_settings_service: SeoSettingsService

    async def handle(self, command: CreateSeoSettingsCommand) -> SeoSettingsEntity:
        return await self.seo_settings_service.create(command.seo_settings)
