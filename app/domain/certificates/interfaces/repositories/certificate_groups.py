from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.certificates.entities.certificate_groups import CertificateGroupEntity


class BaseCertificateGroupRepository(ABC):
    @abstractmethod
    async def add(self, certificate_group: CertificateGroupEntity) -> CertificateGroupEntity: ...

    @abstractmethod
    async def get_by_id(self, certificate_group_id: UUID) -> CertificateGroupEntity | None: ...

    @abstractmethod
    async def get_by_title(self, title: str, section: str) -> CertificateGroupEntity | None: ...

    @abstractmethod
    async def update(self, certificate_group: CertificateGroupEntity) -> None: ...

    @abstractmethod
    async def delete(self, certificate_group_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> AsyncIterable[CertificateGroupEntity]: ...

    @abstractmethod
    async def count_many(
        self,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> int: ...
