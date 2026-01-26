from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.services.certificates import CertificateService


@dataclass(frozen=True)
class DeleteCertificateCommand(BaseCommand):
    certificate_id: UUID


@dataclass(frozen=True)
class DeleteCertificateCommandHandler(
    BaseCommandHandler[DeleteCertificateCommand, None],
):
    certificate_service: CertificateService

    async def handle(self, command: DeleteCertificateCommand) -> None:
        await self.certificate_service.delete(command.certificate_id)
