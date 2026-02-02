from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.members.entities import MemberEntity
from domain.members.services import MemberService


@dataclass(frozen=True)
class GetMemberByIdQuery(BaseQuery):
    member_id: UUID


@dataclass(frozen=True)
class GetMemberByIdQueryHandler(
    BaseQueryHandler[GetMemberByIdQuery, MemberEntity],
):
    member_service: MemberService

    async def handle(self, query: GetMemberByIdQuery) -> MemberEntity:
        return await self.member_service.get_by_id(query.member_id)
