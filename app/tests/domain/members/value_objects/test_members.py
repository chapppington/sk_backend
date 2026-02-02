import pytest

from domain.members.exceptions.members import (
    MemberImageEmptyException,
    MemberNameEmptyException,
    MemberPositionEmptyException,
)
from domain.members.value_objects.members import (
    MemberEmailValueObject,
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Иван Иванов", "Иван Иванов"),
        ("Петр Петров", "Петр Петров"),
    ],
)
def test_member_name_valid(value, expected):
    name = MemberNameValueObject(value)
    assert name.as_generic_type() == expected


def test_member_name_invalid():
    with pytest.raises(MemberNameEmptyException):
        MemberNameValueObject("")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Генеральный директор", "Генеральный директор"),
        ("Менеджер", "Менеджер"),
    ],
)
def test_member_position_valid(value, expected):
    position = MemberPositionValueObject(value)
    assert position.as_generic_type() == expected


def test_member_position_invalid():
    with pytest.raises(MemberPositionEmptyException):
        MemberPositionValueObject("")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("team-member-1.jpg", "team-member-1.jpg"),
        ("/images/member.png", "/images/member.png"),
    ],
)
def test_member_image_valid(value, expected):
    image = MemberImageValueObject(value)
    assert image.as_generic_type() == expected


def test_member_image_invalid():
    with pytest.raises(MemberImageEmptyException):
        MemberImageValueObject("")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("ivan@example.com", "ivan@example.com"),
        (None, None),
    ],
)
def test_member_email_valid(value, expected):
    email = MemberEmailValueObject(value)
    assert email.as_generic_type() == expected
