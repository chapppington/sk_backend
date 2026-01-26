from domain.certificates.entities import ItemEntity
from domain.certificates.value_objects.items import (
    ContentValueObject,
    SectionValueObject,
    TitleValueObject,
)


def test_item_entity_creation():
    section = SectionValueObject("Сертификаты")
    title = TitleValueObject("Сертификат соответствия ГОСТ")
    content = ContentValueObject("Описание сертификата соответствия")

    item = ItemEntity(
        section=section,
        title=title,
        content=content,
    )

    assert item.section.as_generic_type() == "Сертификаты"
    assert item.title.as_generic_type() == "Сертификат соответствия ГОСТ"
    assert item.content.as_generic_type() == "Описание сертификата соответствия"
    assert item.oid is not None
    assert item.created_at is not None
    assert item.updated_at is not None
    assert item.order == 0
    assert item.is_active is True
    assert item.certificates == []


def test_item_entity_creation_with_custom_values():
    section = SectionValueObject("Декларации")
    title = TitleValueObject("Декларация соответствия")
    content = ContentValueObject("Описание декларации")
    order = 5
    is_active = False

    item = ItemEntity(
        section=section,
        title=title,
        content=content,
        order=order,
        is_active=is_active,
    )

    assert item.section.as_generic_type() == "Декларации"
    assert item.title.as_generic_type() == "Декларация соответствия"
    assert item.content.as_generic_type() == "Описание декларации"
    assert item.order == 5
    assert item.is_active is False
    assert item.oid is not None
    assert item.created_at is not None
    assert item.updated_at is not None


def test_item_entity_with_different_sections():
    sections = ["Декларации", "Сертификаты", "Бухгалтерские документы", "Юридические документы", "Опросные листы"]

    for section_name in sections:
        section = SectionValueObject(section_name)
        title = TitleValueObject(f"Заголовок для {section_name}")
        content = ContentValueObject(f"Содержание для {section_name}")

        item = ItemEntity(
            section=section,
            title=title,
            content=content,
        )

        assert item.section.as_generic_type() == section_name
        assert item.title.as_generic_type() == f"Заголовок для {section_name}"
        assert item.content.as_generic_type() == f"Содержание для {section_name}"
