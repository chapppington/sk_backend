from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.members.value_objects.members import (
    MemberEmailValueObject,
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


@dataclass(eq=False)
class MemberEntity(BaseEntity):
    name: MemberNameValueObject
    position: MemberPositionValueObject
    image: MemberImageValueObject
    order: int
    email: MemberEmailValueObject | None = None
