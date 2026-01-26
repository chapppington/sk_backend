from collections.abc import AsyncIterable
from dataclasses import dataclass
from uuid import UUID

from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.interfaces.repositories.certificates import BaseCertificateRepository
from infrastructure.database.converters.certificates.mongo import (
    certificate_document_to_entity,
    certificate_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoCertificateRepository(BaseMongoRepository, BaseCertificateRepository):
    collection_name: str = "certificates"

    async def add(self, certificate: CertificateEntity, certificate_group_id: UUID) -> CertificateEntity:
        document = certificate_entity_to_document(certificate, certificate_group_id)
        await self.collection.insert_one(document)
        return certificate

    async def get_by_id(self, certificate_id: UUID) -> CertificateEntity | None:
        document = await self.collection.find_one({"oid": str(certificate_id)})
        if not document:
            return None
        return certificate_document_to_entity(document)

    async def get_by_title(self, title: str, certificate_group_id: UUID) -> CertificateEntity | None:
        document = await self.collection.find_one({"title": title, "certificate_group_id": str(certificate_group_id)})
        if not document:
            return None
        return certificate_document_to_entity(document)

    async def get_certificate_group_id_by_certificate_id(self, certificate_id: UUID) -> UUID | None:
        document = await self.collection.find_one({"oid": str(certificate_id)}, {"certificate_group_id": 1})
        if not document or "certificate_group_id" not in document:
            return None
        return UUID(document["certificate_group_id"])

    async def update(self, certificate: CertificateEntity) -> None:
        existing_doc = await self.collection.find_one({"oid": str(certificate.oid)}, {"certificate_group_id": 1})
        if not existing_doc:
            raise ValueError(f"Certificate with id {certificate.oid} not found")

        certificate_group_id = UUID(existing_doc["certificate_group_id"])
        document = certificate_entity_to_document(certificate, certificate_group_id)
        await self.collection.update_one(
            {"oid": str(certificate.oid)},
            {"$set": document},
        )

    async def delete(self, certificate_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(certificate_id)})

    def _build_find_query(
        self,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> dict:
        query = {}

        if certificate_group_id:
            query["certificate_group_id"] = str(certificate_group_id)

        if search:
            query["title"] = {"$regex": search, "$options": "i"}

        return query

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> AsyncIterable[CertificateEntity]:
        query = self._build_find_query(certificate_group_id, search)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield certificate_document_to_entity(document)

    async def count_many(
        self,
        certificate_group_id: UUID | None = None,
        search: str | None = None,
    ) -> int:
        query = self._build_find_query(certificate_group_id, search)
        return await self.collection.count_documents(query)
