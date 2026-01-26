from uuid import uuid4

import pytest

from application.certificates.commands import (
    CreateCertificateCommand,
    CreateCertificateGroupCommand,
    UpdateCertificateCommand,
)
from application.certificates.queries import GetCertificateByIdQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.exceptions.certificates import (
    CertificateAlreadyExistsException,
    CertificateNotFoundException,
)
from domain.certificates.value_objects.certificates import CertificateTitleValueObject


@pytest.mark.asyncio
async def test_update_certificate_command_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity: CertificateEntity,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    create_cert_result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=valid_certificate_entity,
            certificate_group_id=created_group.oid,
        ),
    )
    created_certificate: CertificateEntity = create_cert_result

    updated_certificate = CertificateEntity(
        title=CertificateTitleValueObject(value="Updated Title"),
        link=created_certificate.link,
        order=created_certificate.order,
    )

    update_command = UpdateCertificateCommand(
        certificate_id=created_certificate.oid,
        certificate=updated_certificate,
    )
    update_result, *_ = await mediator.handle_command(update_command)

    updated: CertificateEntity = update_result

    assert updated.oid == created_certificate.oid
    assert updated.title.as_generic_type() == "Updated Title"
    assert updated.link.as_generic_type() == created_certificate.link.as_generic_type()

    retrieved_certificate = await mediator.handle_query(
        GetCertificateByIdQuery(certificate_id=created_certificate.oid),
    )

    assert retrieved_certificate.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_certificate_command_not_found(
    mediator: Mediator,
    valid_certificate_entity: CertificateEntity,
):
    non_existent_id = uuid4()
    update_command = UpdateCertificateCommand(
        certificate_id=non_existent_id,
        certificate=valid_certificate_entity,
    )

    with pytest.raises(CertificateNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.certificate_id == non_existent_id


@pytest.mark.asyncio
async def test_update_certificate_command_duplicate_title(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity: CertificateEntity,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    certificate1 = CertificateEntity(
        title=CertificateTitleValueObject(value="First Certificate"),
        link=valid_certificate_entity.link,
        order=1,
    )

    certificate2 = CertificateEntity(
        title=CertificateTitleValueObject(value="Second Certificate"),
        link=valid_certificate_entity.link,
        order=2,
    )

    create_result1, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=certificate1,
            certificate_group_id=created_group.oid,
        ),
    )
    created_certificate1: CertificateEntity = create_result1

    create_result2, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=certificate2,
            certificate_group_id=created_group.oid,
        ),
    )
    created_certificate2: CertificateEntity = create_result2

    updated_certificate = CertificateEntity(
        title=created_certificate2.title,
        link=created_certificate1.link,
        order=created_certificate1.order,
    )

    update_command = UpdateCertificateCommand(
        certificate_id=created_certificate1.oid,
        certificate=updated_certificate,
    )

    with pytest.raises(CertificateAlreadyExistsException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.title == created_certificate2.title.as_generic_type()
