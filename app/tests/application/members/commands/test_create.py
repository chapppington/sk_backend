import pytest

from application.mediator import Mediator
from application.members.commands import CreateMemberCommand
from application.members.queries import GetMemberByIdQuery
from domain.members.entities import MemberEntity


@pytest.mark.asyncio
async def test_create_member_command_success(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    command = CreateMemberCommand(member=valid_member_entity)
    result, *_ = await mediator.handle_command(command)

    member: MemberEntity = result

    assert member is not None
    assert member.name.as_generic_type() == valid_member_entity.name.as_generic_type()
    assert member.position.as_generic_type() == valid_member_entity.position.as_generic_type()
    assert member.image.as_generic_type() == valid_member_entity.image.as_generic_type()
    assert member.order == valid_member_entity.order
    assert member.email is not None and member.email.as_generic_type() == valid_member_entity.email.as_generic_type()
    assert member.oid is not None

    retrieved = await mediator.handle_query(GetMemberByIdQuery(member_id=member.oid))
    assert retrieved.oid == member.oid
    assert retrieved.name.as_generic_type() == valid_member_entity.name.as_generic_type()


@pytest.mark.asyncio
async def test_create_member_command_without_email_success(
    mediator: Mediator,
    valid_member_entity_without_email: MemberEntity,
):
    command = CreateMemberCommand(member=valid_member_entity_without_email)
    result, *_ = await mediator.handle_command(command)

    member: MemberEntity = result

    assert member is not None
    assert member.email is None
    assert member.name.as_generic_type() == valid_member_entity_without_email.name.as_generic_type()

    retrieved = await mediator.handle_query(GetMemberByIdQuery(member_id=member.oid))
    assert retrieved.oid == member.oid
