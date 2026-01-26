from datetime import datetime
from uuid import UUID

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


def certificate_group_entity_to_document(entity: CertificateGroupEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "section": entity.section.as_generic_type(),
        "title": entity.title.as_generic_type(),
        "content": entity.content.as_generic_type(),
        "order": entity.order,
        "is_active": entity.is_active,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def certificate_group_document_to_entity(document: dict) -> CertificateGroupEntity:
    return CertificateGroupEntity(
        oid=UUID(document["oid"]),
        section=SectionValueObject(value=document["section"]),
        title=TitleValueObject(value=document["title"]),
        content=ContentValueObject(value=document["content"]),
        order=document.get("order", 0),
        is_active=document.get("is_active", True),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )


def certificate_entity_to_document(entity: CertificateEntity, certificate_group_id: UUID) -> dict:
    return {
        "oid": str(entity.oid),
        "certificate_group_id": str(certificate_group_id),
        "title": entity.title.as_generic_type(),
        "link": entity.link.as_generic_type(),
        "order": entity.order,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def certificate_document_to_entity(document: dict) -> CertificateEntity:
    return CertificateEntity(
        oid=UUID(document["oid"]),
        title=CertificateTitleValueObject(value=document["title"]),
        link=CertificateLinkValueObject(value=document["link"]),
        order=document["order"],
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
