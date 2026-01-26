from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.certificates.exceptions.items import (
    ContentEmptyException,
    SectionInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)


MAX_TITLE_LENGTH = 255

VALID_SECTIONS = {
    "Декларации",
    "Сертификаты",
    "Бухгалтерские документы",
    "Юридические документы",
    "Опросные листы",
}


@dataclass(frozen=True)
class SectionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if self.value not in VALID_SECTIONS:
            raise SectionInvalidException(section=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class TitleValueObject(BaseValueObject):
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


@dataclass(frozen=True)
class ContentValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise ContentEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)
