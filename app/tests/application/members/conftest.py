import pytest

from domain.members.entities import MemberEntity
from domain.members.value_objects.members import (
    MemberEmailValueObject,
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


@pytest.fixture
def valid_member_entity() -> MemberEntity:
    return MemberEntity(
        name=MemberNameValueObject("Иван Иванов"),
        position=MemberPositionValueObject("Генеральный директор"),
        image=MemberImageValueObject("team-member-1.jpg"),
        order=1,
        email=MemberEmailValueObject("ivan@example.com"),
    )


@pytest.fixture
def valid_member_entity_without_email() -> MemberEntity:
    return MemberEntity(
        name=MemberNameValueObject("Петр Петров"),
        position=MemberPositionValueObject("Менеджер"),
        image=MemberImageValueObject("team-member-2.jpg"),
        order=2,
    )
