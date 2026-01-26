from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class ItemException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с пунктами"


@dataclass(eq=False)
class TitleEmptyException(ItemException):
    @property
    def message(self) -> str:
        return "Заголовок не может быть пустым"


@dataclass(eq=False)
class TitleTooLongException(ItemException):
    title_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Заголовок слишком длинный. Текущая длина: {self.title_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class ContentEmptyException(ItemException):
    @property
    def message(self) -> str:
        return "Содержание не может быть пустым"


@dataclass(eq=False)
class ItemNotFoundException(ItemException):
    item_id: UUID

    @property
    def message(self) -> str:
        return f"Пункт с id {self.item_id} не найден"


@dataclass(eq=False)
class ItemAlreadyExistsException(ItemException):
    title: str

    @property
    def message(self) -> str:
        return f"Пункт с названием '{self.title}' уже существует"


@dataclass(eq=False)
class SectionInvalidException(ItemException):
    section: str

    @property
    def message(self) -> str:
        return f"Невалидная секция '{self.section}'"
