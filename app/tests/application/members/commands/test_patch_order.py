from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.members.commands import (
    CreateMemberCommand,
    PatchMemberOrderCommand,
)
from application.members.queries import GetMemberByIdQuery
from domain.members.entities import MemberEntity
from domain.members.exceptions import MemberNotFoundException


@pytest.mark.asyncio
async def test_patch_member_order_command_success(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    create_result, *_ = await mediator.handle_command(CreateMemberCommand(member=valid_member_entity))
    created: MemberEntity = create_result

    result, *_ = await mediator.handle_command(
        PatchMemberOrderCommand(member_id=created.oid, order=10),
    )

    assert result.oid == created.oid
    assert result.order == 10

    retrieved = await mediator.handle_query(GetMemberByIdQuery(member_id=created.oid))
    assert retrieved.order == 10


@pytest.mark.asyncio
async def test_patch_member_order_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(MemberNotFoundException) as exc_info:
        await mediator.handle_command(
            PatchMemberOrderCommand(member_id=non_existent_id, order=5),
        )

    assert exc_info.value.member_id == non_existent_id
