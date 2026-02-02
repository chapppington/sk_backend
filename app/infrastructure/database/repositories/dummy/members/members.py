from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.members.entities import MemberEntity
from domain.members.interfaces.repository import BaseMemberRepository


@dataclass
class DummyInMemoryMemberRepository(BaseMemberRepository):
    _saved_members: list[MemberEntity] = field(default_factory=list, kw_only=True)

    async def add(self, member: MemberEntity) -> MemberEntity:
        self._saved_members.append(member)
        return member

    async def get_by_id(self, member_id: UUID) -> MemberEntity | None:
        try:
            return next(member for member in self._saved_members if member.oid == member_id)
        except StopIteration:
            return None

    async def update(self, member: MemberEntity) -> None:
        for i, saved_member in enumerate(self._saved_members):
            if saved_member.oid == member.oid:
                self._saved_members[i] = member
                return
        raise ValueError(f"Member with id {member.oid} not found")

    async def delete(self, member_id: UUID) -> None:
        self._saved_members = [member for member in self._saved_members if member.oid != member_id]

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> AsyncIterable[MemberEntity]:
        sorted_members = self._saved_members.copy()
        reverse = sort_order == -1

        if sort_field == "order":
            sorted_members.sort(key=lambda x: x.order, reverse=reverse)
        elif sort_field == "name":
            sorted_members.sort(key=lambda x: x.name.as_generic_type(), reverse=reverse)
        elif sort_field == "position":
            sorted_members.sort(key=lambda x: x.position.as_generic_type(), reverse=reverse)
        elif sort_field == "created_at":
            sorted_members.sort(key=lambda x: x.created_at, reverse=reverse)
        else:
            sorted_members.sort(key=lambda x: x.order, reverse=reverse)

        paginated_members = sorted_members[offset : offset + limit]
        for member in paginated_members:
            yield member

    async def count_many(self) -> int:
        return len(self._saved_members)
