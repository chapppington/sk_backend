from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.value_objects.certificate_groups import (
    ContentValueObject,
    SectionValueObject,
    TitleValueObject,
)
from domain.certificates.value_objects.certificates import (
    CertificateLinkValueObject,
    CertificateTitleValueObject,
)


class CertificateResponseSchema(BaseModel):
    oid: UUID
    title: str
    link: str
    order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: CertificateEntity) -> "CertificateResponseSchema":
        return cls(
            oid=entity.oid,
            title=entity.title.as_generic_type(),
            link=entity.link.as_generic_type(),
            order=entity.order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class CertificateOrderPatchSchema(BaseModel):
    order: int


class CertificateRequestSchema(BaseModel):
    title: str
    link: str
    order: int = 0

    def to_entity(self) -> CertificateEntity:
        return CertificateEntity(
            title=CertificateTitleValueObject(value=self.title),
            link=CertificateLinkValueObject(value=self.link),
            order=self.order,
        )


class CertificateGroupResponseSchema(BaseModel):
    oid: UUID
    section: str
    title: str
    content: str
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: CertificateGroupEntity) -> "CertificateGroupResponseSchema":
        return cls(
            oid=entity.oid,
            section=entity.section.as_generic_type(),
            title=entity.title.as_generic_type(),
            content=entity.content.as_generic_type(),
            order=entity.order,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class CertificateGroupOrderPatchSchema(BaseModel):
    order: int


class CertificateGroupRequestSchema(BaseModel):
    section: str
    title: str
    content: str
    order: int = 0
    is_active: bool = True

    def to_entity(self) -> CertificateGroupEntity:
        return CertificateGroupEntity(
            section=SectionValueObject(value=self.section),
            title=TitleValueObject(value=self.title),
            content=ContentValueObject(value=self.content),
            order=self.order,
            is_active=self.is_active,
        )
