from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.exceptions.certificate_groups import (
    CertificateGroupAlreadyExistsException,
    CertificateGroupNotFoundException,
)
from domain.certificates.interfaces.repositories.certificate_groups import BaseCertificateGroupRepository


@dataclass
class CertificateGroupService:
    certificate_group_repository: BaseCertificateGroupRepository

    async def create(
        self,
        certificate_group: CertificateGroupEntity,
    ) -> CertificateGroupEntity:
        title = certificate_group.title.as_generic_type()
        section = certificate_group.section.as_generic_type()
        existing_certificate_group = await self.certificate_group_repository.get_by_title(title, section)

        if existing_certificate_group:
            raise CertificateGroupAlreadyExistsException(title=title)

        await self.certificate_group_repository.add(certificate_group)

        return certificate_group

    async def get_by_id(
        self,
        certificate_group_id: UUID,
    ) -> CertificateGroupEntity:
        certificate_group = await self.certificate_group_repository.get_by_id(certificate_group_id)

        if not certificate_group:
            raise CertificateGroupNotFoundException(certificate_group_id=certificate_group_id)

        return certificate_group

    async def check_exists(
        self,
        certificate_group_id: UUID,
    ) -> None:
        await self.get_by_id(certificate_group_id)

    async def update(
        self,
        certificate_group: CertificateGroupEntity,
    ) -> CertificateGroupEntity:
        existing_certificate_group = await self.get_by_id(certificate_group.oid)
        current_title = existing_certificate_group.title.as_generic_type()
        new_title = certificate_group.title.as_generic_type()

        if new_title != current_title:
            section = certificate_group.section.as_generic_type()
            existing_certificate_group = await self.certificate_group_repository.get_by_title(new_title, section)

            if existing_certificate_group and existing_certificate_group.oid != certificate_group.oid:
                raise CertificateGroupAlreadyExistsException(title=new_title)

        await self.certificate_group_repository.update(certificate_group)

        return certificate_group

    async def delete(
        self,
        certificate_group_id: UUID,
    ) -> None:
        await self.check_exists(certificate_group_id)
        await self.certificate_group_repository.delete(certificate_group_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        section: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> list[CertificateGroupEntity]:
        certificate_groups_iterable = self.certificate_group_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
            section=section,
            is_active=is_active,
        )
        return [certificate_group async for certificate_group in certificate_groups_iterable]

    async def count_many(
        self,
        search: Optional[str] = None,
        section: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> int:
        return await self.certificate_group_repository.count_many(
            search=search,
            section=section,
            is_active=is_active,
        )
