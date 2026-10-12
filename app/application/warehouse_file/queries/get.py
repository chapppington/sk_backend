from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.warehouse_file.entities import WarehouseFileEntity
from domain.warehouse_file.services import WarehouseFileService


@dataclass(frozen=True)
class GetWarehouseFileQuery(BaseQuery):
    pass


@dataclass(frozen=True)
class GetWarehouseFileQueryHandler(
    BaseQueryHandler[GetWarehouseFileQuery, WarehouseFileEntity | None],
):
    warehouse_file_service: WarehouseFileService

    async def handle(self, query: GetWarehouseFileQuery) -> WarehouseFileEntity | None:
        return await self.warehouse_file_service.get()
