from dataclasses import dataclass
from uuid import UUID

from domain.users.entities.users import UserEntity
from domain.users.interfaces.repository import BaseUserRepository
from infrastructure.database.converters.users.mongo import (
    user_document_to_entity,
    user_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoRepository


@dataclass
class MongoUserRepository(BaseMongoRepository, BaseUserRepository):
    collection_name: str = "users"

    async def add(self, user: UserEntity) -> None:
        document = user_entity_to_document(user)
        await self.collection.insert_one(document)

    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        document = await self.collection.find_one({"oid": str(user_id)})
        if not document:
            return None
        return user_document_to_entity(document)

    async def get_by_email(self, email: str) -> UserEntity | None:
        document = await self.collection.find_one({"email": email.lower()})
        if not document:
            return None
        return user_document_to_entity(document)
