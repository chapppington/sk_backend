import pytest
from faker import Faker

from application.certificates.commands import (
    CreateCertificateCommand,
    CreateCertificateGroupCommand,
)
from application.certificates.queries import GetCertificateByIdQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.exceptions.certificates import CertificateAlreadyExistsException
from domain.certificates.value_objects.certificates import CertificateLinkValueObject


@pytest.mark.asyncio
async def test_create_certificate_command_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity: CertificateEntity,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    command = CreateCertificateCommand(
        certificate=valid_certificate_entity,
        certificate_group_id=created_group.oid,
    )
    result, *_ = await mediator.handle_command(command)

    certificate: CertificateEntity = result

    assert certificate is not None
    assert certificate.title.as_generic_type() == valid_certificate_entity.title.as_generic_type()
    assert certificate.link.as_generic_type() == valid_certificate_entity.link.as_generic_type()
    assert certificate.order == valid_certificate_entity.order
    assert certificate.oid is not None

    retrieved_certificate = await mediator.handle_query(
        GetCertificateByIdQuery(certificate_id=certificate.oid),
    )

    assert retrieved_certificate.oid == certificate.oid
    assert retrieved_certificate.title.as_generic_type() == valid_certificate_entity.title.as_generic_type()


@pytest.mark.asyncio
async def test_create_certificate_command_duplicate_title(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity: CertificateEntity,
    faker: Faker,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    command = CreateCertificateCommand(
        certificate=valid_certificate_entity,
        certificate_group_id=created_group.oid,
    )
    await mediator.handle_command(command)

    duplicate_certificate = CertificateEntity(
        title=valid_certificate_entity.title,
        link=CertificateLinkValueObject(value=faker.url()),
        order=faker.random_int(min=0, max=100),
    )

    with pytest.raises(CertificateAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=duplicate_certificate,
                certificate_group_id=created_group.oid,
            ),
        )

    assert exc_info.value.title == valid_certificate_entity.title.as_generic_type()
