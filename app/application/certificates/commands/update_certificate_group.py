from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.services.certificate_groups import CertificateGroupService


@dataclass(frozen=True)
class UpdateCertificateGroupCommand(BaseCommand):
    certificate_group_id: UUID
    certificate_group: CertificateGroupEntity


@dataclass(frozen=True)
class UpdateCertificateGroupCommandHandler(
    BaseCommandHandler[UpdateCertificateGroupCommand, CertificateGroupEntity],
):
    certificate_group_service: CertificateGroupService

    async def handle(self, command: UpdateCertificateGroupCommand) -> CertificateGroupEntity:
        existing_certificate_group = await self.certificate_group_service.get_by_id(command.certificate_group_id)

        updated_certificate_group = CertificateGroupEntity(
            oid=existing_certificate_group.oid,
            created_at=existing_certificate_group.created_at,
            section=command.certificate_group.section,
            title=command.certificate_group.title,
            content=command.certificate_group.content,
            order=command.certificate_group.order,
            certificates=command.certificate_group.certificates,
            is_active=command.certificate_group.is_active,
        )

        return await self.certificate_group_service.update(updated_certificate_group)
