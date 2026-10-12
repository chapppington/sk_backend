from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.warehouse_file.entities import WarehouseFileEntity


class WarehouseFileResponseSchema(BaseModel):
    oid: UUID
    file_url: str
    file_name: str | None = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: WarehouseFileEntity) -> "WarehouseFileResponseSchema":
        return cls(
            oid=entity.oid,
            file_url=entity.file_url,
            file_name=entity.file_name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class WarehouseFileRequestSchema(BaseModel):
    file_url: str
    file_name: str | None = None
