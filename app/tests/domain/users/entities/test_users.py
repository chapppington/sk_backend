from domain.users.entities import UserEntity
from domain.users.value_objects import (
    EmailValueObject,
    UserNameValueObject,
)


def test_user_entity_creation():
    email = EmailValueObject("test@example.com")
    name = UserNameValueObject("Test User")
    password = "hashed_password_123"

    user = UserEntity(
        email=email,
        hashed_password=password,
        name=name,
    )

    assert user.email.as_generic_type() == "test@example.com"
    assert user.hashed_password == password
    assert user.name.as_generic_type() == "Test User"
    assert user.oid is not None
    assert user.created_at is not None
    assert user.updated_at is not None
