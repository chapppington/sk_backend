from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class DeletePortfolioCommand(BaseCommand):
    portfolio_id: UUID


@dataclass(frozen=True)
class DeletePortfolioCommandHandler(
    BaseCommandHandler[DeletePortfolioCommand, None],
):
    portfolio_service: PortfolioService

    async def handle(self, command: DeletePortfolioCommand) -> None:
        await self.portfolio_service.delete(command.portfolio_id)
