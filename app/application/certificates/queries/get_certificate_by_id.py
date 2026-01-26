from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.services.certificates import CertificateService


@dataclass(frozen=True)
class GetCertificateByIdQuery(BaseQuery):
    certificate_id: UUID


@dataclass(frozen=True)
class GetCertificateByIdQueryHandler(
    BaseQueryHandler[GetCertificateByIdQuery, CertificateEntity],
):
    certificate_service: CertificateService

    async def handle(
        self,
        query: GetCertificateByIdQuery,
    ) -> CertificateEntity:
        return await self.certificate_service.get_by_id(
            certificate_id=query.certificate_id,
        )
