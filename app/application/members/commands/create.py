from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.members.entities import MemberEntity
from domain.members.services import MemberService


@dataclass(frozen=True)
class CreateMemberCommand(BaseCommand):
    member: MemberEntity


@dataclass(frozen=True)
class CreateMemberCommandHandler(
    BaseCommandHandler[CreateMemberCommand, MemberEntity],
):
    member_service: MemberService

    async def handle(self, command: CreateMemberCommand) -> MemberEntity:
        return await self.member_service.create(command.member)
