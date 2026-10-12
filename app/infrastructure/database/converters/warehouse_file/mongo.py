from datetime import datetime
from uuid import UUID

from domain.warehouse_file.entities import WarehouseFileEntity


def warehouse_file_entity_to_document(entity: WarehouseFileEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "file_url": entity.file_url,
        "file_name": entity.file_name,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def warehouse_file_document_to_entity(document: dict) -> WarehouseFileEntity:
    return WarehouseFileEntity(
        oid=UUID(document["oid"]),
        file_url=document["file_url"],
        file_name=document.get("file_name"),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
