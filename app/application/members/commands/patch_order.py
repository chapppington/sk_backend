from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.members.entities import MemberEntity
from domain.members.services import MemberService


@dataclass(frozen=True)
class PatchMemberOrderCommand(BaseCommand):
    member_id: UUID
    order: int


@dataclass(frozen=True)
class PatchMemberOrderCommandHandler(
    BaseCommandHandler[PatchMemberOrderCommand, MemberEntity],
):
    member_service: MemberService

    async def handle(self, command: PatchMemberOrderCommand) -> MemberEntity:
        return await self.member_service.update_order(
            member_id=command.member_id,
            order=command.order,
        )
