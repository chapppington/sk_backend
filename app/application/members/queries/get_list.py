import asyncio
from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.members.entities import MemberEntity
from domain.members.services import MemberService


@dataclass(frozen=True)
class GetMemberListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int


@dataclass(frozen=True)
class GetMemberListQueryHandler(
    BaseQueryHandler[GetMemberListQuery, tuple[list[MemberEntity], int]],
):
    member_service: MemberService

    async def handle(
        self,
        query: GetMemberListQuery,
    ) -> tuple[list[MemberEntity], int]:
        members_task = asyncio.create_task(
            self.member_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
            ),
        )
        count_task = asyncio.create_task(self.member_service.count_many())
        return await members_task, await count_task
