from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.interfaces.repositories.certificate_groups import BaseCertificateGroupRepository


@dataclass
class DummyInMemoryCertificateGroupRepository(BaseCertificateGroupRepository):
    _saved_certificate_groups: list[CertificateGroupEntity] = field(default_factory=list, kw_only=True)

    async def add(self, certificate_group: CertificateGroupEntity) -> CertificateGroupEntity:
        self._saved_certificate_groups.append(certificate_group)
        return certificate_group

    async def get_by_id(self, certificate_group_id: UUID) -> CertificateGroupEntity | None:
        try:
            return next(
                certificate_group
                for certificate_group in self._saved_certificate_groups
                if certificate_group.oid == certificate_group_id
            )
        except StopIteration:
            return None

    async def get_by_title(self, title: str, section: str) -> CertificateGroupEntity | None:
        try:
            return next(
                certificate_group
                for certificate_group in self._saved_certificate_groups
                if certificate_group.title.as_generic_type() == title
                and certificate_group.section.as_generic_type() == section
            )
        except StopIteration:
            return None

    async def update(self, certificate_group: CertificateGroupEntity) -> None:
        for i, saved_certificate_group in enumerate(self._saved_certificate_groups):
            if saved_certificate_group.oid == certificate_group.oid:
                self._saved_certificate_groups[i] = certificate_group
                return
        raise ValueError(f"CertificateGroup with id {certificate_group.oid} not found")

    async def delete(self, certificate_group_id: UUID) -> None:
        self._saved_certificate_groups = [
            certificate_group
            for certificate_group in self._saved_certificate_groups
            if certificate_group.oid != certificate_group_id
        ]

    def _build_find_query(
        self,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> list[CertificateGroupEntity]:
        filtered_certificate_groups = self._saved_certificate_groups.copy()

        if section:
            filtered_certificate_groups = [
                certificate_group
                for certificate_group in filtered_certificate_groups
                if certificate_group.section.as_generic_type() == section
            ]

        if is_active is not None:
            filtered_certificate_groups = [
                certificate_group
                for certificate_group in filtered_certificate_groups
                if certificate_group.is_active == is_active
            ]

        if search:
            search_lower = search.lower()
            filtered_certificate_groups = [
                certificate_group
                for certificate_group in filtered_certificate_groups
                if (
                    search_lower in certificate_group.title.as_generic_type().lower()
                    or search_lower in certificate_group.content.as_generic_type().lower()
                    or search_lower in certificate_group.section.as_generic_type().lower()
                )
            ]

        return filtered_certificate_groups

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> AsyncIterable[CertificateGroupEntity]:
        filtered_certificate_groups = self._build_find_query(search, section, is_active)

        reverse = sort_order == -1

        if sort_field == "order":
            filtered_certificate_groups.sort(key=lambda x: x.order, reverse=reverse)
        elif sort_field == "created_at":
            filtered_certificate_groups.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "title":
            filtered_certificate_groups.sort(key=lambda x: x.title.as_generic_type(), reverse=reverse)
        elif sort_field == "section":
            filtered_certificate_groups.sort(key=lambda x: x.section.as_generic_type(), reverse=reverse)
        else:
            filtered_certificate_groups.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_certificate_groups = filtered_certificate_groups[offset : offset + limit]

        for certificate_group in paginated_certificate_groups:
            yield certificate_group

    async def count_many(
        self,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> int:
        filtered_certificate_groups = self._build_find_query(search, section, is_active)
        return len(filtered_certificate_groups)
