from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class MemberException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с членами команды"


@dataclass(eq=False)
class MemberNameEmptyException(MemberException):
    @property
    def message(self) -> str:
        return "Имя члена команды не может быть пустым"


@dataclass(eq=False)
class MemberPositionEmptyException(MemberException):
    @property
    def message(self) -> str:
        return "Должность члена команды не может быть пустой"


@dataclass(eq=False)
class MemberImageEmptyException(MemberException):
    @property
    def message(self) -> str:
        return "Изображение члена команды не может быть пустым"


@dataclass(eq=False)
class MemberNotFoundException(MemberException):
    member_id: UUID

    @property
    def message(self) -> str:
        return f"Член команды с id {self.member_id} не найден"
