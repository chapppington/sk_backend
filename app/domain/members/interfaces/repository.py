from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.members.entities import MemberEntity


class BaseMemberRepository(ABC):
    @abstractmethod
    async def add(self, member: MemberEntity) -> MemberEntity: ...

    @abstractmethod
    async def get_by_id(self, member_id: UUID) -> MemberEntity | None: ...

    @abstractmethod
    async def update(self, member: MemberEntity) -> None: ...

    @abstractmethod
    async def update_order(self, member_id: UUID, order: int) -> None: ...

    @abstractmethod
    async def delete(self, member_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> AsyncIterable[MemberEntity]: ...

    @abstractmethod
    async def count_many(self) -> int: ...
