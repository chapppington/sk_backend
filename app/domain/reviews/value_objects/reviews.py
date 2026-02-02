from dataclasses import dataclass
from typing import Optional

from domain.base.value_object import BaseValueObject
from domain.reviews.exceptions.reviews import (
    ReviewCategoryInvalidException,
    ReviewNameEmptyException,
)


VALID_REVIEW_CATEGORIES = {
    "Сотрудники",
    "Клиенты",
}


@dataclass(frozen=True)
class ReviewCategoryValueObject(BaseValueObject):
    value: str

    def validate(self):
        if self.value not in VALID_REVIEW_CATEGORIES:
            raise ReviewCategoryInvalidException(category=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ReviewNameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise ReviewNameEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ReviewPositionValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class ReviewImageValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class ReviewTextValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class ReviewShortTextValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class ReviewContentUrlValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value
