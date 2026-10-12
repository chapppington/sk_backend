from dataclasses import dataclass

from domain.warehouse_file.constants import WAREHOUSE_FILE_SINGLETON_OID
from domain.warehouse_file.entities import WarehouseFileEntity
from domain.warehouse_file.exceptions import WarehouseFileUrlEmptyException
from domain.warehouse_file.interfaces.repository import BaseWarehouseFileRepository


@dataclass
class WarehouseFileService:
    warehouse_file_repository: BaseWarehouseFileRepository

    async def get(self) -> WarehouseFileEntity | None:
        return await self.warehouse_file_repository.get()

    async def upsert(self, file_url: str, file_name: str | None = None) -> WarehouseFileEntity:
        normalized_url = file_url.strip()
        if not normalized_url:
            raise WarehouseFileUrlEmptyException()

        existing = await self.warehouse_file_repository.get()
        normalized_name = file_name.strip() if file_name and file_name.strip() else None

        if existing:
            entity = WarehouseFileEntity(
                oid=existing.oid,
                created_at=existing.created_at,
                file_url=normalized_url,
                file_name=normalized_name,
            )
        else:
            entity = WarehouseFileEntity(
                oid=WAREHOUSE_FILE_SINGLETON_OID,
                file_url=normalized_url,
                file_name=normalized_name,
            )

        return await self.warehouse_file_repository.upsert(entity)
