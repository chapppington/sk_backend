import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.services.certificate_groups import CertificateGroupService


@dataclass(frozen=True)
class GetCertificateGroupsListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    section: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass(frozen=True)
class GetCertificateGroupsListQueryHandler(
    BaseQueryHandler[GetCertificateGroupsListQuery, tuple[list[CertificateGroupEntity], int]],
):
    certificate_group_service: CertificateGroupService

    async def handle(
        self,
        query: GetCertificateGroupsListQuery,
    ) -> tuple[list[CertificateGroupEntity], int]:
        certificate_groups_task = asyncio.create_task(
            self.certificate_group_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                search=query.search,
                section=query.section,
                is_active=query.is_active,
            ),
        )
        count_task = asyncio.create_task(
            self.certificate_group_service.count_many(
                search=query.search,
                section=query.section,
                is_active=query.is_active,
            ),
        )

        return await certificate_groups_task, await count_task
