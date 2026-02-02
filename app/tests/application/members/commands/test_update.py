from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.members.commands import (
    CreateMemberCommand,
    UpdateMemberCommand,
)
from application.members.queries import GetMemberByIdQuery
from domain.members.entities import MemberEntity
from domain.members.exceptions import MemberNotFoundException
from domain.members.value_objects.members import (
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


@pytest.mark.asyncio
async def test_update_member_command_success(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    create_result, *_ = await mediator.handle_command(CreateMemberCommand(member=valid_member_entity))
    created: MemberEntity = create_result

    updated_entity = MemberEntity(
        name=MemberNameValueObject("Обновленное Имя"),
        position=MemberPositionValueObject("Директор"),
        image=MemberImageValueObject("updated.jpg"),
        order=5,
        email=created.email,
    )

    update_command = UpdateMemberCommand(member_id=created.oid, member=updated_entity)
    update_result, *_ = await mediator.handle_command(update_command)

    result: MemberEntity = update_result

    assert result.oid == created.oid
    assert result.name.as_generic_type() == "Обновленное Имя"
    assert result.position.as_generic_type() == "Директор"
    assert result.order == 5

    retrieved = await mediator.handle_query(GetMemberByIdQuery(member_id=created.oid))
    assert retrieved.name.as_generic_type() == "Обновленное Имя"


@pytest.mark.asyncio
async def test_update_member_command_not_found(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    non_existent_id = uuid4()
    command = UpdateMemberCommand(member_id=non_existent_id, member=valid_member_entity)

    with pytest.raises(MemberNotFoundException) as exc_info:
        await mediator.handle_command(command)

    assert exc_info.value.member_id == non_existent_id
