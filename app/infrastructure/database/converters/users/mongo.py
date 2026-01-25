from datetime import datetime
from uuid import UUID

from domain.users.entities.users import UserEntity
from domain.users.value_objects.users import (
    EmailValueObject,
    UserNameValueObject,
)


def user_entity_to_document(entity: UserEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "email": entity.email.as_generic_type(),
        "hashed_password": entity.hashed_password,
        "name": entity.name.as_generic_type(),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def user_document_to_entity(document: dict) -> UserEntity:
    return UserEntity(
        oid=UUID(document["oid"]),
        email=EmailValueObject(value=document["email"]),
        hashed_password=document["hashed_password"],
        name=UserNameValueObject(value=document["name"]),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
