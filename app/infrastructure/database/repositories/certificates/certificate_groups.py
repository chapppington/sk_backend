from collections.abc import AsyncIterable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.interfaces.repositories.certificate_groups import BaseCertificateGroupRepository
from infrastructure.database.converters.certificates.mongo import (
    certificate_group_document_to_entity,
    certificate_group_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoCertificateGroupRepository(BaseMongoRepository, BaseCertificateGroupRepository):
    collection_name: str = "certificate_groups"

    async def add(self, certificate_group: CertificateGroupEntity) -> CertificateGroupEntity:
        document = certificate_group_entity_to_document(certificate_group)
        await self.collection.insert_one(document)
        return certificate_group

    async def get_by_id(self, certificate_group_id: UUID) -> CertificateGroupEntity | None:
        document = await self.collection.find_one({"oid": str(certificate_group_id)})
        if not document:
            return None
        return certificate_group_document_to_entity(document)

    async def get_by_title(self, title: str, section: str) -> CertificateGroupEntity | None:
        document = await self.collection.find_one({"title": title, "section": section})
        if not document:
            return None
        return certificate_group_document_to_entity(document)

    async def update(self, certificate_group: CertificateGroupEntity) -> None:
        document = certificate_group_entity_to_document(certificate_group)
        await self.collection.update_one(
            {"oid": str(certificate_group.oid)},
            {"$set": document},
        )

    async def update_order(self, certificate_group_id: UUID, order: int) -> None:
        await self.collection.update_one(
            {"oid": str(certificate_group_id)},
            {"$set": {"order": order, "updated_at": datetime.now().isoformat()}},
        )

    async def delete(self, certificate_group_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(certificate_group_id)})

    def _build_find_query(
        self,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> dict:
        query = {}

        if section:
            query["section"] = section

        if is_active is not None:
            query["is_active"] = is_active

        if search:
            search_query = {
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"content": {"$regex": search, "$options": "i"}},
                    {"section": {"$regex": search, "$options": "i"}},
                ],
            }
            query.update(search_query)

        return query

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
        query = self._build_find_query(search, section, is_active)
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield certificate_group_document_to_entity(document)

    async def count_many(
        self,
        search: str | None = None,
        section: str | None = None,
        is_active: bool | None = None,
    ) -> int:
        query = self._build_find_query(search, section, is_active)
        return await self.collection.count_documents(query)
