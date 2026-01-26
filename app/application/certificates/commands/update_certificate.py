from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.services.certificates import CertificateService


@dataclass(frozen=True)
class UpdateCertificateCommand(BaseCommand):
    certificate_id: UUID
    certificate: CertificateEntity


@dataclass(frozen=True)
class UpdateCertificateCommandHandler(
    BaseCommandHandler[UpdateCertificateCommand, CertificateEntity],
):
    certificate_service: CertificateService

    async def handle(self, command: UpdateCertificateCommand) -> CertificateEntity:
        existing_certificate = await self.certificate_service.get_by_id(command.certificate_id)

        updated_certificate = CertificateEntity(
            oid=existing_certificate.oid,
            created_at=existing_certificate.created_at,
            title=command.certificate.title,
            link=command.certificate.link,
            order=command.certificate.order,
        )

        return await self.certificate_service.update(updated_certificate)
