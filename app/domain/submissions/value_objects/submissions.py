import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.submissions.exceptions import (
    EmailInvalidException,
    FormTypeInvalidException,
    NameEmptyException,
)


VALID_FORM_TYPES = {"Опросный лист", "Отклик на вакансию", "Обращение"}


@dataclass(frozen=True)
class FormTypeValueObject(BaseValueObject):
    value: str

    def validate(self):
        if self.value not in VALID_FORM_TYPES:
            raise FormTypeInvalidException(form_type=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class NameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise NameEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class EmailValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        if self.value is not None:
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, self.value):
                raise EmailInvalidException(email=self.value)

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class PhoneValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None


@dataclass(frozen=True)
class CommentsValueObject(BaseValueObject):
    value: str | None

    def validate(self):
        pass

    def as_generic_type(self) -> str | None:
        return self.value if self.value else None
