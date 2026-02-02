from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.members.services import MemberService


@dataclass(frozen=True)
class DeleteMemberCommand(BaseCommand):
    member_id: UUID


@dataclass(frozen=True)
class DeleteMemberCommandHandler(
    BaseCommandHandler[DeleteMemberCommand, None],
):
    member_service: MemberService

    async def handle(self, command: DeleteMemberCommand) -> None:
        await self.member_service.delete(command.member_id)
