from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.exceptions.certificates import (
    CertificateAlreadyExistsException,
    CertificateNotFoundException,
)
from domain.certificates.interfaces.repositories.certificates import BaseCertificateRepository


@dataclass
class CertificateService:
    certificate_repository: BaseCertificateRepository

    async def create(
        self,
        certificate: CertificateEntity,
        certificate_group_id: UUID,
    ) -> CertificateEntity:
        title = certificate.title.as_generic_type()
        existing_certificate = await self.certificate_repository.get_by_title(title, certificate_group_id)

        if existing_certificate:
            raise CertificateAlreadyExistsException(title=title, category="")

        await self.certificate_repository.add(certificate, certificate_group_id)

        return certificate

    async def get_by_id(
        self,
        certificate_id: UUID,
    ) -> CertificateEntity:
        certificate = await self.certificate_repository.get_by_id(certificate_id)

        if not certificate:
            raise CertificateNotFoundException(certificate_id=certificate_id)

        return certificate

    async def check_exists(
        self,
        certificate_id: UUID,
    ) -> None:
        await self.get_by_id(certificate_id)

    async def update(
        self,
        certificate: CertificateEntity,
    ) -> CertificateEntity:
        existing_certificate = await self.get_by_id(certificate.oid)
        current_title = existing_certificate.title.as_generic_type()
        new_title = certificate.title.as_generic_type()

        if new_title != current_title:
            certificate_group_id = await self.certificate_repository.get_certificate_group_id_by_certificate_id(
                certificate.oid,
            )
            if certificate_group_id:
                existing_certificate = await self.certificate_repository.get_by_title(new_title, certificate_group_id)
                if existing_certificate and existing_certificate.oid != certificate.oid:
                    raise CertificateAlreadyExistsException(title=new_title, category="")

        await self.certificate_repository.update(certificate)

        return certificate

    async def update_order(
        self,
        certificate_id: UUID,
        order: int,
    ) -> CertificateEntity:
        await self.get_by_id(certificate_id)
        await self.certificate_repository.update_order(certificate_id, order)
        updated = await self.certificate_repository.get_by_id(certificate_id)
        assert updated is not None
        return updated

    async def delete(
        self,
        certificate_id: UUID,
    ) -> None:
        await self.check_exists(certificate_id)
        await self.certificate_repository.delete(certificate_id)

    async def delete_all_by_certificate_group_id(
        self,
        certificate_group_id: UUID,
    ) -> None:
        await self.certificate_repository.delete_all_by_certificate_group_id(certificate_group_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        certificate_group_id: Optional[UUID] = None,
        search: Optional[str] = None,
    ) -> list[CertificateEntity]:
        certificates_iterable = self.certificate_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            certificate_group_id=certificate_group_id,
            search=search,
        )
        return [certificate async for certificate in certificates_iterable]

    async def count_many(
        self,
        certificate_group_id: Optional[UUID] = None,
        search: Optional[str] = None,
    ) -> int:
        return await self.certificate_repository.count_many(
            certificate_group_id=certificate_group_id,
            search=search,
        )
