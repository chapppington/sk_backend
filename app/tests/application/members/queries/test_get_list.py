import pytest

from application.mediator import Mediator
from application.members.commands import CreateMemberCommand
from application.members.queries import GetMemberListQuery
from domain.members.entities import MemberEntity


@pytest.mark.asyncio
async def test_get_member_list_query_success(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    for i in range(3):
        member = MemberEntity(
            name=valid_member_entity.name,
            position=valid_member_entity.position,
            image=valid_member_entity.image,
            order=i + 1,
            email=valid_member_entity.email,
        )
        await mediator.handle_command(CreateMemberCommand(member=member))

    members_list, total = await mediator.handle_query(
        GetMemberListQuery(
            sort_field="order",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(members_list) == 3
    assert total == 3
    assert all(isinstance(m, MemberEntity) for m in members_list)


@pytest.mark.asyncio
async def test_get_member_list_query_with_pagination(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    for i in range(5):
        member = MemberEntity(
            name=valid_member_entity.name,
            position=valid_member_entity.position,
            image=valid_member_entity.image,
            order=i + 1,
            email=valid_member_entity.email,
        )
        await mediator.handle_command(CreateMemberCommand(member=member))

    members_list, total = await mediator.handle_query(
        GetMemberListQuery(
            sort_field="order",
            sort_order=1,
            offset=0,
            limit=2,
        ),
    )

    assert len(members_list) == 2
    assert total == 5

    members_list, total = await mediator.handle_query(
        GetMemberListQuery(
            sort_field="order",
            sort_order=1,
            offset=2,
            limit=2,
        ),
    )

    assert len(members_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_member_list_query_with_sorting(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    for order_val in (3, 1, 2):
        member = MemberEntity(
            name=valid_member_entity.name,
            position=valid_member_entity.position,
            image=valid_member_entity.image,
            order=order_val,
            email=valid_member_entity.email,
        )
        await mediator.handle_command(CreateMemberCommand(member=member))

    members_list, total = await mediator.handle_query(
        GetMemberListQuery(
            sort_field="order",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(members_list) == 3
    assert total == 3
    assert members_list[0].order <= members_list[1].order <= members_list[2].order


@pytest.mark.asyncio
async def test_get_member_list_query_count_only(
    mediator: Mediator,
    valid_member_entity: MemberEntity,
):
    for i in range(4):
        member = MemberEntity(
            name=valid_member_entity.name,
            position=valid_member_entity.position,
            image=valid_member_entity.image,
            order=i + 1,
            email=valid_member_entity.email,
        )
        await mediator.handle_command(CreateMemberCommand(member=member))

    _, total = await mediator.handle_query(
        GetMemberListQuery(
            sort_field="order",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 4


@pytest.mark.asyncio
async def test_get_member_list_query_empty(
    mediator: Mediator,
):
    members_list, total = await mediator.handle_query(
        GetMemberListQuery(
            sort_field="order",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(members_list) == 0
    assert total == 0
