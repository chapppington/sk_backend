from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class UserException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с пользователем"


@dataclass(eq=False)
class EmptyEmailException(UserException):
    @property
    def message(self) -> str:
        return "Email не может быть пустым"


@dataclass(eq=False)
class InvalidEmailException(UserException):
    email: str

    @property
    def message(self) -> str:
        return f"Недопустимый формат email: {self.email}"


@dataclass(eq=False)
class EmptyUserNameException(UserException):
    @property
    def message(self) -> str:
        return "Имя пользователя не может быть пустым"


@dataclass(eq=False)
class UserNameTooLongException(UserException):
    name_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Имя пользователя слишком длинное. Текущая длина: {self.name_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class EmptyPasswordException(UserException):
    @property
    def message(self) -> str:
        return "Пароль не может быть пустым"


@dataclass(eq=False)
class PasswordTooShortException(UserException):
    password_length: int
    min_length: int

    @property
    def message(self) -> str:
        return (
            f"Пароль слишком короткий. Текущая длина: {self.password_length}, "
            f"минимально требуемая длина: {self.min_length}"
        )


@dataclass(eq=False)
class InvalidPasswordException(UserException):
    reason: str

    @property
    def message(self) -> str:
        return f"Недопустимый пароль: {self.reason}"


@dataclass(eq=False)
class UserNotFoundException(UserException):
    user_id: UUID

    @property
    def message(self) -> str:
        return f"Пользователь с id {self.user_id} не найден"


@dataclass(eq=False)
class UserAlreadyExistsException(UserException):
    email: str

    @property
    def message(self) -> str:
        return f"Пользователь с email '{self.email}' уже существует"


@dataclass(eq=False)
class InvalidCredentialsException(UserException):
    @property
    def message(self) -> str:
        return "Неверные учетные данные"
