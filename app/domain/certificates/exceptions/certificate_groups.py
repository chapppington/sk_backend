from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class CertificateGroupException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с группами сертификатов"


@dataclass(eq=False)
class TitleEmptyException(CertificateGroupException):
    @property
    def message(self) -> str:
        return "Заголовок не может быть пустым"


@dataclass(eq=False)
class TitleTooLongException(CertificateGroupException):
    title_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Заголовок слишком длинный. Текущая длина: {self.title_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class ContentEmptyException(CertificateGroupException):
    @property
    def message(self) -> str:
        return "Содержание не может быть пустым"


@dataclass(eq=False)
class CertificateGroupNotFoundException(CertificateGroupException):
    certificate_group_id: UUID

    @property
    def message(self) -> str:
        return f"Группа сертификатов с id {self.certificate_group_id} не найдена"


@dataclass(eq=False)
class CertificateGroupAlreadyExistsException(CertificateGroupException):
    title: str

    @property
    def message(self) -> str:
        return f"Группа сертификатов с названием '{self.title}' уже существует"


@dataclass(eq=False)
class SectionInvalidException(CertificateGroupException):
    section: str

    @property
    def message(self) -> str:
        return f"Невалидная секция '{self.section}'"
