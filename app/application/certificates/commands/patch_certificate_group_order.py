from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.services.certificate_groups import CertificateGroupService


@dataclass(frozen=True)
class PatchCertificateGroupOrderCommand(BaseCommand):
    certificate_group_id: UUID
    order: int


@dataclass(frozen=True)
class PatchCertificateGroupOrderCommandHandler(
    BaseCommandHandler[PatchCertificateGroupOrderCommand, CertificateGroupEntity],
):
    certificate_group_service: CertificateGroupService

    async def handle(self, command: PatchCertificateGroupOrderCommand) -> CertificateGroupEntity:
        return await self.certificate_group_service.update_order(
            certificate_group_id=command.certificate_group_id,
            order=command.order,
        )
