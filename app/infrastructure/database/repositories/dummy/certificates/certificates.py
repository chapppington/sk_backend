from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
    replace,
)
from datetime import datetime
from uuid import UUID

from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.interfaces.repositories.certificates import BaseCertificateRepository


@dataclass
class DummyInMemoryCertificateRepository(BaseCertificateRepository):
    _saved_certificates: list[tuple[CertificateEntity, UUID]] = field(default_factory=list, kw_only=True)

    async def add(self, certificate: CertificateEntity, certificate_group_id: UUID) -> CertificateEntity:
        self._saved_certificates.append((certificate, certificate_group_id))
        return certificate

    async def get_by_id(self, certificate_id: UUID) -> CertificateEntity | None:
        try:
            return next(cert for cert, _ in self._saved_certificates if cert.oid == certificate_id)
        except StopIteration:
            return None

    async def get_by_title(self, title: str, certificate_group_id: UUID) -> CertificateEntity | None:
        try:
            return next(
                cert
                for cert, saved_certificate_group_id in self._saved_certificates
                if cert.title.as_generic_type() == title and saved_certificate_group_id == certificate_group_id
            )
        except StopIteration:
            return None

    async def get_certificate_group_id_by_certificate_id(self, certificate_id: UUID) -> UUID | None:
        try:
            return next(
                certificate_group_id
                for cert, certificate_group_id in self._saved_certificates
                if cert.oid == certificate_id
            )
        except StopIteration:
            return None

    async def update(self, certificate: CertificateEntity) -> None:
        for i, (saved_cert, certificate_group_id) in enumerate(self._saved_certificates):
            if saved_cert.oid == certificate.oid:
                self._saved_certificates[i] = (certificate, certificate_group_id)
                return
        raise ValueError(f"Certificate with id {certificate.oid} not found")

    async def update_order(self, certificate_id: UUID, order: int) -> None:
        for i, (saved_cert, certificate_group_id) in enumerate(self._saved_certificates):
            if saved_cert.oid == certificate_id:
                self._saved_certificates[i] = (
                    replace(saved_cert, order=order, updated_at=datetime.now()),
                    certificate_group_id,
                )
                return
        raise ValueError(f"Certificate with id {certificate_id} not found")

    async def delete(self, certificate_id: UUID) -> None:
        self._saved_certificates = [
            (cert, certificate_group_id)
            for cert, certificate_group_id in self._saved_certificates
            if cert.oid != certificate_id
        ]

    async def delete_all_by_certificate_group_id(self, certificate_group_id: UUID) -> None:
        self._saved_certificates = [
            (cert, group_id) for cert, group_id in self._saved_certificates if group_id != certificate_group_id
        ]

    def _build_find_query(
        self,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> list[tuple[CertificateEntity, UUID]]:
        filtered_certificates = self._saved_certificates.copy()

        if certificate_group_id:
            filtered_certificates = [
                (cert, saved_certificate_group_id)
                for cert, saved_certificate_group_id in filtered_certificates
                if saved_certificate_group_id == certificate_group_id
            ]

        if search:
            search_lower = search.lower()
            filtered_certificates = [
                (cert, saved_certificate_group_id)
                for cert, saved_certificate_group_id in filtered_certificates
                if search_lower in cert.title.as_generic_type().lower()
            ]

        return filtered_certificates

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> AsyncIterable[CertificateEntity]:
        filtered_certificates = self._build_find_query(certificate_group_id, search)

        reverse = sort_order == -1

        if sort_field == "order":
            filtered_certificates.sort(key=lambda x: x[0].order, reverse=reverse)
        elif sort_field == "created_at":
            filtered_certificates.sort(key=lambda x: x[0].created_at, reverse=reverse)
        elif sort_field == "title":
            filtered_certificates.sort(key=lambda x: x[0].title.as_generic_type(), reverse=reverse)
        else:
            filtered_certificates.sort(key=lambda x: x[0].created_at, reverse=reverse)

        paginated_certificates = filtered_certificates[offset : offset + limit]

        for cert, _ in paginated_certificates:
            yield cert

    async def count_many(
        self,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> int:
        filtered_certificates = self._build_find_query(certificate_group_id, search)
        return len(filtered_certificates)
