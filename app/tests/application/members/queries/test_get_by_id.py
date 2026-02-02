from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.members.commands import CreateMemberCommand
from application.members.queries import GetMemberByIdQuery
from domain.members.entities import MemberEntity
from domain.members.exceptions import MemberNotFoundException


@pytest.mark.asyncio
async def test_get_member_by_id_success(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    create_result, *_ = await mediator.handle_command(CreateMemberCommand(member=valid_member_entity))
    created: MemberEntity = create_result

    retrieved = await mediator.handle_query(GetMemberByIdQuery(member_id=created.oid))

    assert retrieved.oid == created.oid
    assert retrieved.name.as_generic_type() == valid_member_entity.name.as_generic_type()
    assert retrieved.position.as_generic_type() == valid_member_entity.position.as_generic_type()


@pytest.mark.asyncio
async def test_get_member_by_id_not_found(mediator: Mediator):
    non_existent_id = uuid4()

    with pytest.raises(MemberNotFoundException) as exc_info:
        await mediator.handle_query(GetMemberByIdQuery(member_id=non_existent_id))

    assert exc_info.value.member_id == non_existent_id
