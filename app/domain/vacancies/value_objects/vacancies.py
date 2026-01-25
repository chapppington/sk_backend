from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.vacancies.exceptions import (
    CategoryInvalidException,
    ExperienceEmptyException,
    RequirementsEmptyException,
    SalaryInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)


VALID_CATEGORIES = {"Кадровый резерв", "Производство", "Продажи и маркетинг", "Офис компании"}

MAX_TITLE_LENGTH = 255
MIN_SALARY = 0


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
class RequirementsValueObject(BaseValueObject):
    value: list[str]

    def validate(self):
        if not self.value:
            raise RequirementsEmptyException()

    def as_generic_type(self) -> list[str]:
        return list(self.value)


@dataclass(frozen=True)
class ExperienceValueObject(BaseValueObject):
    value: list[str]

    def validate(self):
        if not self.value:
            raise ExperienceEmptyException()

    def as_generic_type(self) -> list[str]:
        return list(self.value)


@dataclass(frozen=True)
class SalaryValueObject(BaseValueObject):
    value: int

    def validate(self):
        if self.value < MIN_SALARY:
            raise SalaryInvalidException(salary=self.value)

    def as_generic_type(self) -> int:
        return int(self.value)
