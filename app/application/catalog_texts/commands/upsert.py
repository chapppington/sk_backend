from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.catalog_texts.entities import CatalogTextEntity
from domain.catalog_texts.services import CatalogTextService


@dataclass(frozen=True)
class UpsertCatalogTextCommand(BaseCommand):
    category: str
    content: dict


@dataclass(frozen=True)
class UpsertCatalogTextCommandHandler(BaseCommandHandler[UpsertCatalogTextCommand, CatalogTextEntity]):
    catalog_text_service: CatalogTextService

    async def handle(self, command: UpsertCatalogTextCommand) -> CatalogTextEntity:
        return await self.catalog_text_service.upsert(command.category, command.content)
