from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.services.certificate_groups import CertificateGroupService


@dataclass(frozen=True)
class DeleteCertificateGroupCommand(BaseCommand):
    certificate_group_id: UUID


@dataclass(frozen=True)
class DeleteCertificateGroupCommandHandler(
    BaseCommandHandler[DeleteCertificateGroupCommand, None],
):
    certificate_group_service: CertificateGroupService

    async def handle(self, command: DeleteCertificateGroupCommand) -> None:
        await self.certificate_group_service.delete(command.certificate_group_id)
