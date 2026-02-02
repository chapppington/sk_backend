from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain.members.entities import MemberEntity
from domain.members.value_objects.members import (
    MemberEmailValueObject,
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


class MemberResponseSchema(BaseModel):
    oid: UUID
    name: str
    position: str
    image: str
    order: int
    email: Optional[str] = None
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: MemberEntity) -> "MemberResponseSchema":
        return cls(
            oid=entity.oid,
            name=entity.name.as_generic_type(),
            position=entity.position.as_generic_type(),
            image=entity.image.as_generic_type(),
            order=entity.order,
            email=entity.email.as_generic_type() if entity.email else None,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


class MemberRequestSchema(BaseModel):
    name: str
    position: str
    image: str
    order: int
    email: Optional[str] = None

    def to_entity(self) -> MemberEntity:
        email_vo = MemberEmailValueObject(value=self.email) if self.email is not None else None
        return MemberEntity(
            name=MemberNameValueObject(value=self.name),
            position=MemberPositionValueObject(value=self.position),
            image=MemberImageValueObject(value=self.image),
            order=self.order,
            email=email_vo,
        )


class MemberOrderPatchSchema(BaseModel):
    order: int
