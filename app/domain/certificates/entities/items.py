from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.base.entity import BaseEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.value_objects.items import (
    ContentValueObject,
    TitleValueObject,
)


@dataclass(eq=False)
class ItemEntity(BaseEntity):
    section_id: UUID
    title: TitleValueObject
    content: ContentValueObject
    order: int = 0
    certificates: list[CertificateEntity] = field(default_factory=list)
    is_active: bool = True
