from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.certificates.exceptions.items import (
    TitleEmptyException,
    TitleTooLongException,
)


MAX_TITLE_LENGTH = 255


@dataclass(frozen=True)
class SectionNameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise TitleEmptyException()

        if len(self.value) > MAX_TITLE_LENGTH:
            raise TitleTooLongException(
                title_length=len(self.value),
                max_length=MAX_TITLE_LENGTH,
            )

    def as_generic_type(self) -> str:
        return str(self.value)
