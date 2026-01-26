from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class SectionException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с разделами"


@dataclass(eq=False)
class SectionNotFoundException(SectionException):
    section_id: UUID

    @property
    def message(self) -> str:
        return f"Раздел с id {self.section_id} не найден"


@dataclass(eq=False)
class SectionAlreadyExistsException(SectionException):
    name: str

    @property
    def message(self) -> str:
        return f"Раздел с названием '{self.name}' уже существует"
