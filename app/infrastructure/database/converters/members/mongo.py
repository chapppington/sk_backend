from datetime import datetime
from uuid import UUID

from domain.members.entities import MemberEntity
from domain.members.value_objects.members import (
    MemberEmailValueObject,
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


def member_entity_to_document(entity: MemberEntity) -> dict:
    doc = {
        "oid": str(entity.oid),
        "name": entity.name.as_generic_type(),
        "position": entity.position.as_generic_type(),
        "image": entity.image.as_generic_type(),
        "order": entity.order,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }
    if entity.email is not None:
        doc["email"] = entity.email.as_generic_type()
    else:
        doc["email"] = None
    return doc


def member_document_to_entity(document: dict) -> MemberEntity:
    email_value = document.get("email")
    email = MemberEmailValueObject(value=email_value) if email_value is not None else None
    return MemberEntity(
        oid=UUID(document["oid"]),
        name=MemberNameValueObject(value=document["name"]),
        position=MemberPositionValueObject(value=document["position"]),
        image=MemberImageValueObject(value=document["image"]),
        order=document["order"],
        email=email,
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
