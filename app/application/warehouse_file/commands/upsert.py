from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.warehouse_file.entities import WarehouseFileEntity
from domain.warehouse_file.services import WarehouseFileService


@dataclass(frozen=True)
class UpsertWarehouseFileCommand(BaseCommand):
    file_url: str
    file_name: str | None = None


@dataclass(frozen=True)
class UpsertWarehouseFileCommandHandler(
    BaseCommandHandler[UpsertWarehouseFileCommand, WarehouseFileEntity],
):
    warehouse_file_service: WarehouseFileService

    async def handle(self, command: UpsertWarehouseFileCommand) -> WarehouseFileEntity:
        return await self.warehouse_file_service.upsert(
            file_url=command.file_url,
            file_name=command.file_name,
        )
