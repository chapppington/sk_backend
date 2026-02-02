from collections.abc import AsyncIterable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.members.entities import MemberEntity
from domain.members.interfaces.repository import BaseMemberRepository
from infrastructure.database.converters.members.mongo import (
    member_document_to_entity,
    member_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoMemberRepository(BaseMongoRepository, BaseMemberRepository):
    collection_name: str = "members"

    async def add(self, member: MemberEntity) -> MemberEntity:
        document = member_entity_to_document(member)
        await self.collection.insert_one(document)
        return member

    async def get_by_id(self, member_id: UUID) -> MemberEntity | None:
        document = await self.collection.find_one({"oid": str(member_id)})
        if not document:
            return None
        return member_document_to_entity(document)

    async def update(self, member: MemberEntity) -> None:
        document = member_entity_to_document(member)
        await self.collection.update_one(
            {"oid": str(member.oid)},
            {"$set": document},
        )

    async def update_order(self, member_id: UUID, order: int) -> None:
        await self.collection.update_one(
            {"oid": str(member_id)},
            {"$set": {"order": order, "updated_at": datetime.now().isoformat()}},
        )

    async def delete(self, member_id: UUID) -> None:
        await self.collection.delete_one({"oid": str(member_id)})

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> AsyncIterable[MemberEntity]:
        cursor = self.collection.find({}).sort(sort_field, sort_order).skip(offset).limit(limit)
        async for document in cursor:
            yield member_document_to_entity(document)

    async def count_many(self) -> int:
        return await self.collection.count_documents({})
