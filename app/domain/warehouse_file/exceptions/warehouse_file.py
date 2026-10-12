from dataclasses import dataclass

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class WarehouseFileException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с файлом склада"


@dataclass(eq=False)
class WarehouseFileUrlEmptyException(WarehouseFileException):
    @property
    def message(self) -> str:
        return "URL файла не может быть пустым"
