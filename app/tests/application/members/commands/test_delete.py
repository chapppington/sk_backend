from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.members.commands import (
    CreateMemberCommand,
    DeleteMemberCommand,
)
from application.members.queries import GetMemberByIdQuery
from domain.members.entities import MemberEntity
from domain.members.exceptions import MemberNotFoundException


@pytest.mark.asyncio
async def test_delete_member_command_success(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    create_result, *_ = await mediator.handle_command(CreateMemberCommand(member=valid_member_entity))
    created: MemberEntity = create_result

    await mediator.handle_command(DeleteMemberCommand(member_id=created.oid))

    with pytest.raises(MemberNotFoundException):
        await mediator.handle_query(GetMemberByIdQuery(member_id=created.oid))


@pytest.mark.asyncio
async def test_delete_member_command_not_found(mediator: Mediator):
    non_existent_id = uuid4()

    with pytest.raises(MemberNotFoundException) as exc_info:
        await mediator.handle_command(DeleteMemberCommand(member_id=non_existent_id))

    assert exc_info.value.member_id == non_existent_id
