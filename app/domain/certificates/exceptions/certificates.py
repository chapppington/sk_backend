from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class CertificateException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с сертификатами"


@dataclass(eq=False)
class CertificateTitleEmptyException(CertificateException):
    @property
    def message(self) -> str:
        return "Название сертификата не может быть пустым"


@dataclass(eq=False)
class CertificateLinkEmptyException(CertificateException):
    @property
    def message(self) -> str:
        return "Ссылка на сертификат не может быть пустой"


@dataclass(eq=False)
class CertificateNotFoundException(CertificateException):
    certificate_id: UUID

    @property
    def message(self) -> str:
        return f"Сертификат с id {self.certificate_id} не найден"


@dataclass(eq=False)
class CertificateAlreadyExistsException(CertificateException):
    title: str
    category: str

    @property
    def message(self) -> str:
        return f"Сертификат с названием '{self.title}' в категории '{self.category}' уже существует"
