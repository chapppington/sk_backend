from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.services.certificates import CertificateService


@dataclass(frozen=True)
class PatchCertificateOrderCommand(BaseCommand):
    certificate_id: UUID
    order: int


@dataclass(frozen=True)
class PatchCertificateOrderCommandHandler(
    BaseCommandHandler[PatchCertificateOrderCommand, CertificateEntity],
):
    certificate_service: CertificateService

    async def handle(self, command: PatchCertificateOrderCommand) -> CertificateEntity:
        return await self.certificate_service.update_order(
            certificate_id=command.certificate_id,
            order=command.order,
        )
