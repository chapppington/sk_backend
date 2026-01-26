import asyncio
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.services.certificates import CertificateService


@dataclass(frozen=True)
class GetCertificatesListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    certificate_group_id: Optional[UUID] = None
    search: Optional[str] = None


@dataclass(frozen=True)
class GetCertificatesListQueryHandler(
    BaseQueryHandler[GetCertificatesListQuery, tuple[list[CertificateEntity], int]],
):
    certificate_service: CertificateService

    async def handle(
        self,
        query: GetCertificatesListQuery,
    ) -> tuple[list[CertificateEntity], int]:
        certificates_task = asyncio.create_task(
            self.certificate_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                certificate_group_id=query.certificate_group_id,
                search=query.search,
            ),
        )
        count_task = asyncio.create_task(
            self.certificate_service.count_many(
                certificate_group_id=query.certificate_group_id,
                search=query.search,
            ),
        )

        return await certificates_task, await count_task
