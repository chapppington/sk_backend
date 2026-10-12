from abc import ABC

from domain.warehouse_file.entities import WarehouseFileEntity


class BaseWarehouseFileRepository(ABC):
    async def get(self) -> WarehouseFileEntity | None: ...

    async def upsert(self, entity: WarehouseFileEntity) -> WarehouseFileEntity: ...
