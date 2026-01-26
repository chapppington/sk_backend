import pytest

from application.certificates.commands import CreateCertificateGroupCommand
from application.certificates.queries import GetCertificateGroupsListQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.value_objects.certificate_groups import TitleValueObject


@pytest.mark.asyncio
async def test_get_certificate_groups_list_query_success(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
):
    for _ in range(5):
        certificate_group = valid_certificate_group_entity_with_section("Сертификаты")
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    certificate_groups_list, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(certificate_groups_list) == 5
    assert total == 5
    assert all(isinstance(certificate_group, CertificateGroupEntity) for certificate_group in certificate_groups_list)


@pytest.mark.asyncio
async def test_get_certificate_groups_list_query_with_pagination(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
):
    for _ in range(5):
        certificate_group = valid_certificate_group_entity_with_section()
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    certificate_groups_list, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(certificate_groups_list) == 2
    assert total == 5

    certificate_groups_list, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(certificate_groups_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_certificate_groups_list_query_with_section_filter(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
):
    for _ in range(3):
        certificate_group = valid_certificate_group_entity_with_section("Сертификаты")
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    for _ in range(2):
        certificate_group = valid_certificate_group_entity_with_section("Декларации")
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    certificate_groups_list, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            section="Сертификаты",
        ),
    )

    assert len(certificate_groups_list) == 3
    assert total == 3
    assert all(
        certificate_group.section.as_generic_type() == "Сертификаты" for certificate_group in certificate_groups_list
    )


@pytest.mark.asyncio
async def test_get_certificate_groups_list_query_with_is_active_filter(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
):
    for _ in range(3):
        base_group = valid_certificate_group_entity_with_section("Сертификаты")
        certificate_group = CertificateGroupEntity(
            section=base_group.section,
            title=base_group.title,
            content=base_group.content,
            order=base_group.order,
            certificates=base_group.certificates,
            is_active=True,
        )
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    for _ in range(2):
        base_group = valid_certificate_group_entity_with_section("Сертификаты")
        certificate_group = CertificateGroupEntity(
            section=base_group.section,
            title=base_group.title,
            content=base_group.content,
            order=base_group.order,
            certificates=base_group.certificates,
            is_active=False,
        )
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    certificate_groups_list, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            is_active=True,
        ),
    )

    assert len(certificate_groups_list) == 3
    assert total == 3
    assert all(certificate_group.is_active is True for certificate_group in certificate_groups_list)


@pytest.mark.asyncio
async def test_get_certificate_groups_list_query_with_search(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
):
    certificate_group1 = valid_certificate_group_entity_with_section("Сертификаты")
    certificate_group1 = CertificateGroupEntity(
        section=certificate_group1.section,
        title=TitleValueObject(value="Python Certificate"),
        content=certificate_group1.content,
        order=certificate_group1.order,
        certificates=certificate_group1.certificates,
        is_active=certificate_group1.is_active,
    )
    await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=certificate_group1),
    )

    certificate_group2 = valid_certificate_group_entity_with_section("Сертификаты")
    certificate_group2 = CertificateGroupEntity(
        section=certificate_group2.section,
        title=TitleValueObject(value="JavaScript Certificate"),
        content=certificate_group2.content,
        order=certificate_group2.order,
        certificates=certificate_group2.certificates,
        is_active=certificate_group2.is_active,
    )
    await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=certificate_group2),
    )

    certificate_groups_list, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(certificate_groups_list) == 1
    assert total == 1
    assert "Python" in certificate_groups_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_certificate_groups_list_query_count_only(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
):
    for _ in range(3):
        certificate_group = valid_certificate_group_entity_with_section()
        await mediator.handle_command(
            CreateCertificateGroupCommand(certificate_group=certificate_group),
        )

    _, total = await mediator.handle_query(
        GetCertificateGroupsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3
