from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "Произошла ошибка приложения"


@dataclass(eq=False)
class DomainException(ApplicationException):
    @property
    def message(self) -> str:
        return "Произошла доменная ошибка"
