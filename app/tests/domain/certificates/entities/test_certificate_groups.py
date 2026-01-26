from domain.certificates.entities import CertificateGroupEntity
from domain.certificates.value_objects.certificate_groups import (
    ContentValueObject,
    SectionValueObject,
    TitleValueObject,
)


def test_certificate_group_entity_creation():
    section = SectionValueObject("Сертификаты")
    title = TitleValueObject("Сертификат соответствия ГОСТ")
    content = ContentValueObject("Описание сертификата соответствия")

    certificate_group = CertificateGroupEntity(
        section=section,
        title=title,
        content=content,
    )

    assert certificate_group.section.as_generic_type() == "Сертификаты"
    assert certificate_group.title.as_generic_type() == "Сертификат соответствия ГОСТ"
    assert certificate_group.content.as_generic_type() == "Описание сертификата соответствия"
    assert certificate_group.oid is not None
    assert certificate_group.created_at is not None
    assert certificate_group.updated_at is not None
    assert certificate_group.order == 0
    assert certificate_group.is_active is True
    assert certificate_group.certificates == []


def test_certificate_group_entity_creation_with_custom_values():
    section = SectionValueObject("Декларации")
    title = TitleValueObject("Декларация соответствия")
    content = ContentValueObject("Описание декларации")
    order = 5
    is_active = False

    certificate_group = CertificateGroupEntity(
        section=section,
        title=title,
        content=content,
        order=order,
        is_active=is_active,
    )

    assert certificate_group.section.as_generic_type() == "Декларации"
    assert certificate_group.title.as_generic_type() == "Декларация соответствия"
    assert certificate_group.content.as_generic_type() == "Описание декларации"
    assert certificate_group.order == 5
    assert certificate_group.is_active is False
    assert certificate_group.oid is not None
    assert certificate_group.created_at is not None
    assert certificate_group.updated_at is not None


def test_certificate_group_entity_with_different_sections():
    sections = ["Декларации", "Сертификаты", "Бухгалтерские документы", "Юридические документы", "Опросные листы"]

    for section_name in sections:
        section = SectionValueObject(section_name)
        title = TitleValueObject(f"Заголовок для {section_name}")
        content = ContentValueObject(f"Содержание для {section_name}")

        certificate_group = CertificateGroupEntity(
            section=section,
            title=title,
            content=content,
        )

        assert certificate_group.section.as_generic_type() == section_name
        assert certificate_group.title.as_generic_type() == f"Заголовок для {section_name}"
        assert certificate_group.content.as_generic_type() == f"Содержание для {section_name}"
