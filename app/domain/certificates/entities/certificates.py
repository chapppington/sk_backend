from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.certificates.value_objects.certificates import (
    CertificateLinkValueObject,
    CertificateTitleValueObject,
)


@dataclass(eq=False)
class CertificateEntity(BaseEntity):
    title: CertificateTitleValueObject
    link: CertificateLinkValueObject
    order: int
