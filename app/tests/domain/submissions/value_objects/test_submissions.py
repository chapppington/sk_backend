import pytest

from domain.submissions.exceptions import (
    EmailInvalidException,
    FormTypeInvalidException,
    NameEmptyException,
)
from domain.submissions.value_objects.submissions import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
)


@pytest.mark.parametrize(
    "form_type_value,expected",
    [
        ("Опросный лист", "Опросный лист"),
        ("Отклик на вакансию", "Отклик на вакансию"),
        ("Обращение", "Обращение"),
    ],
)
def test_form_type_valid(form_type_value, expected):
    form_type = FormTypeValueObject(form_type_value)
    assert form_type.as_generic_type() == expected


@pytest.mark.parametrize(
    "form_type_value,exception",
    [
        ("", FormTypeInvalidException),
        ("invalid", FormTypeInvalidException),
        ("Опросный лист ", FormTypeInvalidException),
        ("опросный лист", FormTypeInvalidException),
    ],
)
def test_form_type_invalid(form_type_value, exception):
    with pytest.raises(exception):
        FormTypeValueObject(form_type_value)


@pytest.mark.parametrize(
    "name_value,expected",
    [
        ("Иван Иванов", "Иван Иванов"),
        ("John Doe", "John Doe"),
        ("А", "А"),
        ("A" * 255, "A" * 255),
    ],
)
def test_name_valid(name_value, expected):
    name = NameValueObject(name_value)
    assert name.as_generic_type() == expected


@pytest.mark.parametrize(
    "name_value,exception",
    [
        ("", NameEmptyException),
        ("   ", NameEmptyException),
        ("\t", NameEmptyException),
        ("\n", NameEmptyException),
    ],
)
def test_name_invalid(name_value, exception):
    with pytest.raises(exception):
        NameValueObject(name_value)


@pytest.mark.parametrize(
    "email_value,expected",
    [
        ("test@example.com", "test@example.com"),
        ("user.name@domain.co.uk", "user.name@domain.co.uk"),
        ("admin@test.io", "admin@test.io"),
        (None, None),
    ],
)
def test_email_valid(email_value, expected):
    email = EmailValueObject(email_value)
    assert email.as_generic_type() == expected


@pytest.mark.parametrize(
    "email_value,exception",
    [
        ("invalid-email", EmailInvalidException),
        ("test@", EmailInvalidException),
        ("test@example", EmailInvalidException),
        ("@example.com", EmailInvalidException),
        ("test @example.com", EmailInvalidException),
    ],
)
def test_email_invalid(email_value, exception):
    with pytest.raises(exception):
        EmailValueObject(email_value)


@pytest.mark.parametrize(
    "phone_value,expected",
    [
        ("+7 (999) 123-45-67", "+7 (999) 123-45-67"),
        ("89991234567", "89991234567"),
        ("+1234567890", "+1234567890"),
        (None, None),
        ("", None),
    ],
)
def test_phone_valid(phone_value, expected):
    phone = PhoneValueObject(phone_value)
    assert phone.as_generic_type() == expected


@pytest.mark.parametrize(
    "comments_value,expected",
    [
        ("Some comments", "Some comments"),
        ("", None),
        (None, None),
        ("Long comment text " * 10, "Long comment text " * 10),
    ],
)
def test_comments_valid(comments_value, expected):
    comments = CommentsValueObject(comments_value)
    assert comments.as_generic_type() == expected
