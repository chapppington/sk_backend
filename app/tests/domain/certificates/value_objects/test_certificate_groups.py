import pytest

from domain.certificates.exceptions.certificate_groups import (
    ContentEmptyException,
    SectionInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)
from domain.certificates.value_objects.certificate_groups import (
    ContentValueObject,
    SectionValueObject,
    TitleValueObject,
    VALID_SECTIONS,
)


@pytest.mark.parametrize(
    "section_value,expected",
    [
        ("Декларации", "Декларации"),
        ("Сертификаты", "Сертификаты"),
        ("Бухгалтерские документы", "Бухгалтерские документы"),
        ("Юридические документы", "Юридические документы"),
        ("Опросные листы", "Опросные листы"),
    ],
)
def test_section_valid(section_value, expected):
    section = SectionValueObject(section_value)
    assert section.as_generic_type() == expected


@pytest.mark.parametrize(
    "section_value,exception",
    [
        ("", SectionInvalidException),
        ("invalid", SectionInvalidException),
        ("Сертификат", SectionInvalidException),
        ("Лицензии", SectionInvalidException),
    ],
)
def test_section_invalid(section_value, exception):
    with pytest.raises(exception):
        SectionValueObject(section_value)


def test_section_all_valid_sections():
    for section in VALID_SECTIONS:
        section_obj = SectionValueObject(section)
        assert section_obj.as_generic_type() == section


@pytest.mark.parametrize(
    "title_value,expected",
    [
        ("Название пункта", "Название пункта"),
        ("A" * 255, "A" * 255),
        ("Тестовый заголовок", "Тестовый заголовок"),
    ],
)
def test_title_valid(title_value, expected):
    title = TitleValueObject(title_value)
    assert title.as_generic_type() == expected


@pytest.mark.parametrize(
    "title_value,exception",
    [
        ("", TitleEmptyException),
        ("A" * 256, TitleTooLongException),
        ("A" * 1000, TitleTooLongException),
    ],
)
def test_title_invalid(title_value, exception):
    with pytest.raises(exception):
        TitleValueObject(title_value)


@pytest.mark.parametrize(
    "content_value,expected",
    [
        ("Содержание пункта", "Содержание пункта"),
        ("A" * 1000, "A" * 1000),
        ("Текст с разными символами: !@#$%^&*()", "Текст с разными символами: !@#$%^&*()"),
    ],
)
def test_content_valid(content_value, expected):
    content = ContentValueObject(content_value)
    assert content.as_generic_type() == expected


@pytest.mark.parametrize(
    "content_value,exception",
    [
        ("", ContentEmptyException),
    ],
)
def test_content_invalid(content_value, exception):
    with pytest.raises(exception):
        ContentValueObject(content_value)
