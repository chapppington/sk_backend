from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.services.certificate_groups import CertificateGroupService


@dataclass(frozen=True)
class CreateCertificateGroupCommand(BaseCommand):
    certificate_group: CertificateGroupEntity


@dataclass(frozen=True)
class CreateCertificateGroupCommandHandler(
    BaseCommandHandler[CreateCertificateGroupCommand, CertificateGroupEntity],
):
    certificate_group_service: CertificateGroupService

    async def handle(self, command: CreateCertificateGroupCommand) -> CertificateGroupEntity:
        return await self.certificate_group_service.create(command.certificate_group)
