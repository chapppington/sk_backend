from dataclasses import dataclass
from uuid import UUID

from domain.members.entities import MemberEntity
from domain.members.exceptions import MemberNotFoundException
from domain.members.interfaces.repository import BaseMemberRepository


@dataclass
class MemberService:
    member_repository: BaseMemberRepository

    async def create(self, member: MemberEntity) -> MemberEntity:
        await self.member_repository.add(member)
        return member

    async def get_by_id(self, member_id: UUID) -> MemberEntity:
        member = await self.member_repository.get_by_id(member_id)
        if not member:
            raise MemberNotFoundException(member_id=member_id)
        return member

    async def update(self, member: MemberEntity) -> MemberEntity:
        await self.get_by_id(member.oid)
        await self.member_repository.update(member)
        return member

    async def update_order(self, member_id: UUID, order: int) -> MemberEntity:
        await self.get_by_id(member_id)
        await self.member_repository.update_order(member_id, order)
        updated = await self.member_repository.get_by_id(member_id)
        assert updated is not None
        return updated

    async def delete(self, member_id: UUID) -> None:
        await self.get_by_id(member_id)
        await self.member_repository.delete(member_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> list[MemberEntity]:
        members_iterable = self.member_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
        )
        return [member async for member in members_iterable]

    async def count_many(self) -> int:
        return await self.member_repository.count_many()
