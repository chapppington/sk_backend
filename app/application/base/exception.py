from dataclasses import dataclass

from domain.base.exceptions import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException):
    @property
    def message(self) -> str:
        return "Произошла логическая ошибка"
