import pytest
from faker import Faker

from application.certificates.commands import CreateCertificateGroupCommand
from application.certificates.queries import GetCertificateGroupByIdQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.exceptions.certificate_groups import CertificateGroupAlreadyExistsException
from domain.certificates.value_objects.certificate_groups import ContentValueObject


@pytest.mark.asyncio
async def test_create_certificate_group_command_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
):
    command = CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity)
    result, *_ = await mediator.handle_command(command)

    certificate_group: CertificateGroupEntity = result

    assert certificate_group is not None
    assert certificate_group.section.as_generic_type() == valid_certificate_group_entity.section.as_generic_type()
    assert certificate_group.title.as_generic_type() == valid_certificate_group_entity.title.as_generic_type()
    assert certificate_group.content.as_generic_type() == valid_certificate_group_entity.content.as_generic_type()
    assert certificate_group.oid is not None

    retrieved_certificate_group = await mediator.handle_query(
        GetCertificateGroupByIdQuery(certificate_group_id=certificate_group.oid),
    )

    assert retrieved_certificate_group.oid == certificate_group.oid
    assert retrieved_certificate_group.title.as_generic_type() == valid_certificate_group_entity.title.as_generic_type()


@pytest.mark.asyncio
async def test_create_certificate_group_command_duplicate_title(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    faker: Faker,
):
    command = CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity)
    await mediator.handle_command(command)

    duplicate_certificate_group = CertificateGroupEntity(
        section=valid_certificate_group_entity.section,
        title=valid_certificate_group_entity.title,
        content=ContentValueObject(value=faker.text(max_nb_chars=500)),
    )

    with pytest.raises(CertificateGroupAlreadyExistsException) as exc_info:
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=duplicate_certificate_group))

    assert exc_info.value.title == valid_certificate_group_entity.title.as_generic_type()
