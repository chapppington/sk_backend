from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.certificates.value_objects.sections import SectionNameValueObject


@dataclass(eq=False)
class SectionEntity(BaseEntity):
    name: SectionNameValueObject
    order: int = 0
