from dataclasses import dataclass

from domain.warehouse_file.constants import WAREHOUSE_FILE_SINGLETON_OID
from domain.warehouse_file.entities import WarehouseFileEntity
from domain.warehouse_file.interfaces.repository import BaseWarehouseFileRepository
from infrastructure.database.converters.warehouse_file.mongo import (
    warehouse_file_document_to_entity,
    warehouse_file_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoWarehouseFileRepository(BaseMongoRepository, BaseWarehouseFileRepository):
    collection_name: str = "warehouse_file"

    async def get(self) -> WarehouseFileEntity | None:
        document = await self.collection.find_one({"oid": str(WAREHOUSE_FILE_SINGLETON_OID)})
        if not document:
            return None
        return warehouse_file_document_to_entity(document)

    async def upsert(self, entity: WarehouseFileEntity) -> WarehouseFileEntity:
        document = warehouse_file_entity_to_document(entity)
        await self.collection.replace_one(
            {"oid": str(WAREHOUSE_FILE_SINGLETON_OID)},
            document,
            upsert=True,
        )
        return entity
