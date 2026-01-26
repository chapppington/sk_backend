from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.seo_settings.services import SeoSettingsService


@dataclass(frozen=True)
class DeleteSeoSettingsCommand(BaseCommand):
    seo_settings_id: UUID


@dataclass(frozen=True)
class DeleteSeoSettingsCommandHandler(
    BaseCommandHandler[DeleteSeoSettingsCommand, None],
):
    seo_settings_service: SeoSettingsService

    async def handle(self, command: DeleteSeoSettingsCommand) -> None:
        await self.seo_settings_service.delete(command.seo_settings_id)
