from dataclasses import dataclass

from application.base.exception import LogicException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f"Обработчики команд не зарегистрированы для типа команды: {self.command_type.__name__}"


@dataclass(eq=False)
class QueryHandlerNotRegisteredException(LogicException):
    query_type: type

    @property
    def message(self) -> str:
        return f"Обработчик запроса не зарегистрирован для типа запроса: {self.query_type.__name__}"
