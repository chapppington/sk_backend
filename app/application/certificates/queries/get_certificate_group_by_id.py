from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.services.certificate_groups import CertificateGroupService


@dataclass(frozen=True)
class GetCertificateGroupByIdQuery(BaseQuery):
    certificate_group_id: UUID


@dataclass(frozen=True)
class GetCertificateGroupByIdQueryHandler(
    BaseQueryHandler[GetCertificateGroupByIdQuery, CertificateGroupEntity],
):
    certificate_group_service: CertificateGroupService

    async def handle(
        self,
        query: GetCertificateGroupByIdQuery,
    ) -> CertificateGroupEntity:
        return await self.certificate_group_service.get_by_id(
            certificate_group_id=query.certificate_group_id,
        )
