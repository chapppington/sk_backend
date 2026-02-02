from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.members.entities import MemberEntity
from domain.members.services import MemberService


@dataclass(frozen=True)
class UpdateMemberCommand(BaseCommand):
    member_id: UUID
    member: MemberEntity


@dataclass(frozen=True)
class UpdateMemberCommandHandler(
    BaseCommandHandler[UpdateMemberCommand, MemberEntity],
):
    member_service: MemberService

    async def handle(self, command: UpdateMemberCommand) -> MemberEntity:
        existing_member = await self.member_service.get_by_id(command.member_id)
        updated_member = MemberEntity(
            oid=existing_member.oid,
            created_at=existing_member.created_at,
            name=command.member.name,
            position=command.member.position,
            image=command.member.image,
            order=command.member.order,
            email=command.member.email,
        )
        return await self.member_service.update(updated_member)
