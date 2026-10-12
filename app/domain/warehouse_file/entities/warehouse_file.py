from dataclasses import dataclass

from domain.base.entity import BaseEntity


@dataclass(eq=False)
class WarehouseFileEntity(BaseEntity):
    file_url: str
    file_name: str | None = None
