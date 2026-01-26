from dataclasses import (
    dataclass,
    field,
)

from domain.base.entity import BaseEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.value_objects.certificate_groups import (
    ContentValueObject,
    SectionValueObject,
    TitleValueObject,
)


@dataclass(eq=False)
class CertificateGroupEntity(BaseEntity):
    section: SectionValueObject
    title: TitleValueObject
    content: ContentValueObject
    order: int = 0
    certificates: list[CertificateEntity] = field(default_factory=list)
    is_active: bool = True
