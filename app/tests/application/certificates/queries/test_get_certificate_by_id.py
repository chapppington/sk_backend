from uuid import uuid4

import pytest

from application.certificates.commands import (
    CreateCertificateCommand,
    CreateCertificateGroupCommand,
)
from application.certificates.queries import GetCertificateByIdQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.exceptions.certificates import CertificateNotFoundException


@pytest.mark.asyncio
async def test_get_certificate_by_id_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
    valid_certificate_entity: CertificateEntity,
):
    create_group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_group: CertificateGroupEntity = create_group_result

    create_result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=valid_certificate_entity,
            certificate_group_id=created_group.oid,
        ),
    )
    created_certificate: CertificateEntity = create_result

    retrieved_certificate = await mediator.handle_query(
        GetCertificateByIdQuery(certificate_id=created_certificate.oid),
    )

    assert retrieved_certificate.oid == created_certificate.oid
    assert retrieved_certificate.title.as_generic_type() == valid_certificate_entity.title.as_generic_type()
    assert retrieved_certificate.link.as_generic_type() == valid_certificate_entity.link.as_generic_type()


@pytest.mark.asyncio
async def test_get_certificate_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(CertificateNotFoundException) as exc_info:
        await mediator.handle_query(
            GetCertificateByIdQuery(certificate_id=non_existent_id),
        )

    assert exc_info.value.certificate_id == non_existent_id
