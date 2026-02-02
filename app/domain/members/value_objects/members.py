from dataclasses import dataclass
from typing import Optional

from domain.base.value_object import BaseValueObject
from domain.members.exceptions.members import (
    MemberImageEmptyException,
    MemberNameEmptyException,
    MemberPositionEmptyException,
)


@dataclass(frozen=True)
class MemberNameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise MemberNameEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class MemberPositionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise MemberPositionEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class MemberImageValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise MemberImageEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class MemberEmailValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value
