import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.products.exceptions import (
    CategoryInvalidException,
    DescriptionEmptyException,
    NameEmptyException,
    NameTooLongException,
    PreviewImageUrlInvalidException,
    SlugEmptyException,
    SlugInvalidException,
)


MAX_NAME_LENGTH = 255
MAX_SLUG_LENGTH = 255
VALID_CATEGORIES = {
    "Трансформаторные подстанции",
    "Распределительные устройства среднего напряжения 6(10) кВ",
    "Распределительные устройства низкого напряжения 0,4 кВ",
    "Пункты коммерческого учёта и секционирования воздушных линий электропередач",
    "Электростанции и установки",
}


@dataclass(frozen=True)
class NameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise NameEmptyException()

        if len(self.value) > MAX_NAME_LENGTH:
            raise NameTooLongException(
                name_length=len(self.value),
                max_length=MAX_NAME_LENGTH,
            )

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SlugValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SlugEmptyException()

        if len(self.value) > MAX_SLUG_LENGTH:
            raise SlugInvalidException(slug=self.value)

        slug_pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
        if not re.match(slug_pattern, self.value):
            raise SlugInvalidException(slug=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class DescriptionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise DescriptionEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class CategoryValueObject(BaseValueObject):
    value: str

    def validate(self):
        if self.value not in VALID_CATEGORIES:
            raise CategoryInvalidException(category=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PreviewImageUrlValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise PreviewImageUrlInvalidException(url=self.value)
        if not self.value.startswith(("http://", "https://")):
            raise PreviewImageUrlInvalidException(url=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PreviewImageAltValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        if self.value is None:
            return None
        return str(self.value)
