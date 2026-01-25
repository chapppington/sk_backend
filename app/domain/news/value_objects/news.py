import re
from dataclasses import dataclass
from typing import Optional

from domain.base.value_object import BaseValueObject
from domain.news.exceptions import (
    AltTooLongException,
    CategoryInvalidException,
    ContentEmptyException,
    ReadingTimeInvalidException,
    ShortContentEmptyException,
    ShortContentTooLongException,
    SlugEmptyException,
    SlugInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)


VALID_CATEGORIES = {"Производство", "Разработки", "Полезное", "События", "Наши проекты"}

MAX_TITLE_LENGTH = 255
MAX_SHORT_CONTENT_LENGTH = 500
MAX_ALT_LENGTH = 255


@dataclass(frozen=True)
class CategoryValueObject(BaseValueObject):
    value: str

    def validate(self):
        if self.value not in VALID_CATEGORIES:
            raise CategoryInvalidException(category=self.value)

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
class SlugValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SlugEmptyException()

        slug_pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
        if not re.match(slug_pattern, self.value):
            raise SlugInvalidException(slug=self.value)

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


@dataclass(frozen=True)
class ShortContentValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise ShortContentEmptyException()

        if len(self.value) > MAX_SHORT_CONTENT_LENGTH:
            raise ShortContentTooLongException(
                content_length=len(self.value),
                max_length=MAX_SHORT_CONTENT_LENGTH,
            )

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ImageUrlValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class AltValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        if self.value and len(self.value) > MAX_ALT_LENGTH:
            raise AltTooLongException(
                alt_length=len(self.value),
                max_length=MAX_ALT_LENGTH,
            )

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class ReadingTimeValueObject(BaseValueObject):
    value: int

    def validate(self):
        if self.value <= 0:
            raise ReadingTimeInvalidException(reading_time=self.value)

    def as_generic_type(self) -> int:
        return int(self.value)
