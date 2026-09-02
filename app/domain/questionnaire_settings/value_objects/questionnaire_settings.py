import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.questionnaire_settings.exceptions import (
    PageNameEmptyException,
    QuestionnaireH1EmptyException,
    QuestionnaireSlugInvalidException,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class QuestionnaireSlugValueObject(BaseValueObject):
    value: str

    def validate(self):
        slug = self.value.strip().lower()
        if not slug or not SLUG_PATTERN.fullmatch(slug):
            raise QuestionnaireSlugInvalidException(slug=self.value)

    def as_generic_type(self) -> str:
        return str(self.value.strip().lower())


@dataclass(frozen=True)
class H1ValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value.strip():
            raise QuestionnaireH1EmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class SubtitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        pass

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class BreadcrumbLabelValueObject(BaseValueObject):
    value: str

    def validate(self):
        pass

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PageNameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value.strip():
            raise PageNameEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)
