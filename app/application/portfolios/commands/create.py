from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class CreatePortfolioCommand(BaseCommand):
    portfolio: PortfolioEntity


@dataclass(frozen=True)
class CreatePortfolioCommandHandler(
    BaseCommandHandler[CreatePortfolioCommand, PortfolioEntity],
):
    portfolio_service: PortfolioService

    async def handle(self, command: CreatePortfolioCommand) -> PortfolioEntity:
        return await self.portfolio_service.create(command.portfolio)
