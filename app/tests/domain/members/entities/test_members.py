from domain.members.entities import MemberEntity
from domain.members.value_objects.members import (
    MemberEmailValueObject,
    MemberImageValueObject,
    MemberNameValueObject,
    MemberPositionValueObject,
)


def test_member_entity_creation():
    name = MemberNameValueObject("Иван Иванов")
    position = MemberPositionValueObject("Генеральный директор")
    image = MemberImageValueObject("team-member-1.jpg")
    email = MemberEmailValueObject("ivan.ivanov@example.com")

    member = MemberEntity(
        name=name,
        position=position,
        image=image,
        order=1,
        email=email,
    )

    assert member.name.as_generic_type() == "Иван Иванов"
    assert member.position.as_generic_type() == "Генеральный директор"
    assert member.email.as_generic_type() == "ivan.ivanov@example.com"
    assert member.image.as_generic_type() == "team-member-1.jpg"
    assert member.order == 1
    assert member.oid is not None
    assert member.created_at is not None
    assert member.updated_at is not None


def test_member_entity_creation_without_email():
    name = MemberNameValueObject("Петр Петров")
    position = MemberPositionValueObject("Менеджер")
    image = MemberImageValueObject("team-member-2.jpg")

    member = MemberEntity(
        name=name,
        position=position,
        image=image,
        order=2,
    )

    assert member.name.as_generic_type() == "Петр Петров"
    assert member.position.as_generic_type() == "Менеджер"
    assert member.email is None
    assert member.image.as_generic_type() == "team-member-2.jpg"
    assert member.order == 2
    assert member.oid is not None


def test_member_entity_creation_with_different_orders():
    for order_value in (1, 5, 10):
        member = MemberEntity(
            name=MemberNameValueObject(f"Член команды {order_value}"),
            position=MemberPositionValueObject("Сотрудник"),
            image=MemberImageValueObject(f"member-{order_value}.jpg"),
            order=order_value,
        )
        assert member.order == order_value
        assert member.name.as_generic_type() == f"Член команды {order_value}"
        assert member.oid is not None
