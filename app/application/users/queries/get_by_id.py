from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.users.entities import UserEntity
from domain.users.services import UserService


@dataclass(frozen=True)
class GetUserByIdQuery(BaseQuery):
    user_id: UUID


@dataclass(frozen=True)
class GetUserByIdQueryHandler(
    BaseQueryHandler[GetUserByIdQuery, UserEntity],
):
    user_service: UserService

    async def handle(
        self,
        query: GetUserByIdQuery,
    ) -> UserEntity:
        return await self.user_service.get_by_id(
            user_id=query.user_id,
        )
