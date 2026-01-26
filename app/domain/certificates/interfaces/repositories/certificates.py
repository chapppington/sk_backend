from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.certificates.entities.certificates import CertificateEntity


class BaseCertificateRepository(ABC):
    @abstractmethod
    async def add(self, certificate: CertificateEntity, certificate_group_id: UUID) -> CertificateEntity: ...

    @abstractmethod
    async def get_by_id(self, certificate_id: UUID) -> CertificateEntity | None: ...

    @abstractmethod
    async def get_by_title(self, title: str, certificate_group_id: UUID) -> CertificateEntity | None: ...

    @abstractmethod
    async def get_certificate_group_id_by_certificate_id(self, certificate_id: UUID) -> UUID | None: ...

    @abstractmethod
    async def update(self, certificate: CertificateEntity) -> None: ...

    @abstractmethod
    async def delete(self, certificate_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> AsyncIterable[CertificateEntity]: ...

    @abstractmethod
    async def count_many(
        self,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> int: ...
