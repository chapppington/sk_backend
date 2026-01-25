import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.portfolios.exceptions import (
    DescriptionEmptyException,
    NameEmptyException,
    NameTooLongException,
    PosterUrlInvalidException,
    ReviewImageUrlInvalidException,
    SlugEmptyException,
    SlugInvalidException,
    SolutionDescriptionEmptyException,
    SolutionImageUrlInvalidException,
    SolutionSubdescriptionEmptyException,
    SolutionSubtitleEmptyException,
    SolutionTitleEmptyException,
    TaskDescriptionEmptyException,
    TaskTitleEmptyException,
    VideoUrlInvalidException,
    YearInvalidException,
)


MAX_NAME_LENGTH = 255
MAX_SLUG_LENGTH = 255
MIN_YEAR = 2000
MAX_YEAR = 2100


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
class PosterUrlValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise PosterUrlInvalidException(url=self.value)

        if not self.value.startswith(("http://", "https://")):
            raise PosterUrlInvalidException(url=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class YearValueObject(BaseValueObject):
    value: int

    def validate(self):
        if not (MIN_YEAR <= self.value <= MAX_YEAR):
            raise YearInvalidException(year=self.value)

    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class TaskTitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise TaskTitleEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class TaskDescriptionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise TaskDescriptionEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SolutionTitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SolutionTitleEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SolutionDescriptionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SolutionDescriptionEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SolutionSubtitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SolutionSubtitleEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SolutionSubdescriptionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SolutionSubdescriptionEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SolutionImageUrlValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise SolutionImageUrlInvalidException(url=self.value)

        if not self.value.startswith(("http://", "https://")):
            raise SolutionImageUrlInvalidException(url=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class VideoUrlValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        if self.value is None:
            return
        if not self.value:
            raise VideoUrlInvalidException(url=self.value)
        if not self.value.startswith(("http://", "https://")):
            raise VideoUrlInvalidException(url=self.value)

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class DescriptionValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise DescriptionEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ReviewTitleValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class ReviewTextValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class ReviewNameValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class ReviewImageUrlValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        if self.value and not self.value.startswith(("http://", "https://")):
            raise ReviewImageUrlInvalidException(url=self.value)

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class ReviewRoleValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None
