from uuid import uuid4

import pytest

from application.certificates.commands import (
    CreateCertificateGroupCommand,
    DeleteCertificateGroupCommand,
)
from application.certificates.queries import GetCertificateGroupByIdQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.exceptions.certificate_groups import CertificateGroupNotFoundException


@pytest.mark.asyncio
async def test_delete_certificate_group_command_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
):
    create_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity),
    )
    created_certificate_group: CertificateGroupEntity = create_result

    await mediator.handle_command(
        DeleteCertificateGroupCommand(certificate_group_id=created_certificate_group.oid),
    )

    with pytest.raises(CertificateGroupNotFoundException):
        await mediator.handle_query(
            GetCertificateGroupByIdQuery(certificate_group_id=created_certificate_group.oid),
        )


@pytest.mark.asyncio
async def test_delete_certificate_group_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(CertificateGroupNotFoundException) as exc_info:
        await mediator.handle_command(
            DeleteCertificateGroupCommand(certificate_group_id=non_existent_id),
        )

    assert exc_info.value.certificate_group_id == non_existent_id
