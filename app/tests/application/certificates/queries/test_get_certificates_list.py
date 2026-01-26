import pytest

from application.certificates.commands import (
    CreateCertificateCommand,
    CreateCertificateGroupCommand,
)
from application.certificates.queries import GetCertificatesListQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.value_objects.certificates import CertificateTitleValueObject


@pytest.mark.asyncio
async def test_get_certificates_list_query_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity_factory,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    for _ in range(5):
        certificate = valid_certificate_entity_factory()
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=certificate,
                certificate_group_id=created_group.oid,
            ),
        )

    certificates_list, total = await mediator.handle_query(
        GetCertificatesListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(certificates_list) == 5
    assert total == 5
    assert all(isinstance(certificate, CertificateEntity) for certificate in certificates_list)


@pytest.mark.asyncio
async def test_get_certificates_list_query_with_pagination(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity_factory,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    for _ in range(5):
        certificate = valid_certificate_entity_factory()
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=certificate,
                certificate_group_id=created_group.oid,
            ),
        )

    certificates_list, total = await mediator.handle_query(
        GetCertificatesListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(certificates_list) == 2
    assert total == 5

    certificates_list, total = await mediator.handle_query(
        GetCertificatesListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(certificates_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_certificates_list_query_with_certificate_group_id_filter(
    mediator: Mediator,
    valid_certificate_group_entity_with_section,
    valid_certificate_entity_factory,
):
    certificate_group1_entity = valid_certificate_group_entity_with_section("Сертификаты")
    create_group_result1, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=certificate_group1_entity),
    )
    created_group1: CertificateGroupEntity = create_group_result1

    certificate_group2_entity = valid_certificate_group_entity_with_section("Сертификаты")
    create_group_result2, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=certificate_group2_entity),
    )
    created_group2: CertificateGroupEntity = create_group_result2

    for _ in range(3):
        certificate = valid_certificate_entity_factory()
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=certificate,
                certificate_group_id=created_group1.oid,
            ),
        )

    for _ in range(2):
        certificate = valid_certificate_entity_factory()
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=certificate,
                certificate_group_id=created_group2.oid,
            ),
        )

    certificates_list, total = await mediator.handle_query(
        GetCertificatesListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            certificate_group_id=created_group1.oid,
        ),
    )

    assert len(certificates_list) == 3
    assert total == 3


@pytest.mark.asyncio
async def test_get_certificates_list_query_with_search(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity_factory,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    base_certificate = valid_certificate_entity_factory()
    certificate1 = CertificateEntity(
        title=CertificateTitleValueObject(value="Python Certificate"),
        link=base_certificate.link,
        order=1,
    )
    await mediator.handle_command(
        CreateCertificateCommand(
            certificate=certificate1,
            certificate_group_id=created_group.oid,
        ),
    )

    certificate2 = CertificateEntity(
        title=CertificateTitleValueObject(value="JavaScript Certificate"),
        link=base_certificate.link,
        order=2,
    )
    await mediator.handle_command(
        CreateCertificateCommand(
            certificate=certificate2,
            certificate_group_id=created_group.oid,
        ),
    )

    certificates_list, total = await mediator.handle_query(
        GetCertificatesListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(certificates_list) == 1
    assert total == 1
    assert "Python" in certificates_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_certificates_list_query_count_only(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity_factory,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    for _ in range(3):
        certificate = valid_certificate_entity_factory()
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=certificate,
                certificate_group_id=created_group.oid,
            ),
        )

    _, total = await mediator.handle_query(
        GetCertificatesListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3
