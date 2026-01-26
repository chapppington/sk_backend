from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.services.certificates import CertificateService


@dataclass(frozen=True)
class CreateCertificateCommand(BaseCommand):
    certificate: CertificateEntity
    certificate_group_id: UUID


@dataclass(frozen=True)
class CreateCertificateCommandHandler(
    BaseCommandHandler[CreateCertificateCommand, CertificateEntity],
):
    certificate_service: CertificateService

    async def handle(self, command: CreateCertificateCommand) -> CertificateEntity:
        return await self.certificate_service.create(
            certificate=command.certificate,
            certificate_group_id=command.certificate_group_id,
        )
