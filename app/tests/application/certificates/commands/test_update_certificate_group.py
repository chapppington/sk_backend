from uuid import uuid4

import pytest

from application.certificates.commands import (
    CreateCertificateGroupCommand,
    UpdateCertificateGroupCommand,
)
from application.certificates.queries import GetCertificateGroupByIdQuery
from application.mediator import Mediator
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.exceptions.certificate_groups import (
    CertificateGroupAlreadyExistsException,
    CertificateGroupNotFoundException,
)
from domain.certificates.value_objects.certificate_groups import TitleValueObject


@pytest.mark.asyncio
async def test_update_certificate_group_command_success(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
):
    create_command = CreateCertificateGroupCommand(certificate_group=valid_certificate_group_entity)
    create_result, *_ = await mediator.handle_command(create_command)
    created_certificate_group: CertificateGroupEntity = create_result

    updated_certificate_group = CertificateGroupEntity(
        section=created_certificate_group.section,
        title=TitleValueObject(value="Updated Title"),
        content=created_certificate_group.content,
        order=created_certificate_group.order,
        certificates=created_certificate_group.certificates,
        is_active=created_certificate_group.is_active,
    )

    update_command = UpdateCertificateGroupCommand(
        certificate_group_id=created_certificate_group.oid,
        certificate_group=updated_certificate_group,
    )
    update_result, *_ = await mediator.handle_command(update_command)

    updated: CertificateGroupEntity = update_result

    assert updated.oid == created_certificate_group.oid
    assert updated.title.as_generic_type() == "Updated Title"
    assert updated.section.as_generic_type() == created_certificate_group.section.as_generic_type()

    retrieved_certificate_group = await mediator.handle_query(
        GetCertificateGroupByIdQuery(certificate_group_id=created_certificate_group.oid),
    )

    assert retrieved_certificate_group.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_certificate_group_command_not_found(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
):
    non_existent_id = uuid4()
    update_command = UpdateCertificateGroupCommand(
        certificate_group_id=non_existent_id,
        certificate_group=valid_certificate_group_entity,
    )

    with pytest.raises(CertificateGroupNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.certificate_group_id == non_existent_id


@pytest.mark.asyncio
async def test_update_certificate_group_command_duplicate_title(
    mediator: Mediator,
    valid_certificate_group_entity: CertificateGroupEntity,
):
    certificate_group1 = CertificateGroupEntity(
        section=valid_certificate_group_entity.section,
        title=TitleValueObject(value="First Group"),
        content=valid_certificate_group_entity.content,
    )

    certificate_group2 = CertificateGroupEntity(
        section=valid_certificate_group_entity.section,
        title=TitleValueObject(value="Second Group"),
        content=valid_certificate_group_entity.content,
    )

    create_result1, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=certificate_group1),
    )
    created_certificate_group1: CertificateGroupEntity = create_result1

    create_result2, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=certificate_group2),
    )
    created_certificate_group2: CertificateGroupEntity = create_result2

    updated_certificate_group = CertificateGroupEntity(
        section=created_certificate_group1.section,
        title=created_certificate_group2.title,
        content=created_certificate_group1.content,
        order=created_certificate_group1.order,
        certificates=created_certificate_group1.certificates,
        is_active=created_certificate_group1.is_active,
    )

    update_command = UpdateCertificateGroupCommand(
        certificate_group_id=created_certificate_group1.oid,
        certificate_group=updated_certificate_group,
    )

    with pytest.raises(CertificateGroupAlreadyExistsException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.title == created_certificate_group2.title.as_generic_type()
