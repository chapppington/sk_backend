from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.certificates.exceptions.certificates import (
    CertificateLinkEmptyException,
    CertificateTitleEmptyException,
)


@dataclass(frozen=True)
class CertificateTitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise CertificateTitleEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class CertificateLinkValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise CertificateLinkEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)
