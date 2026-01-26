from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.services.portfolios import PortfolioService
from domain.products.entities import ProductEntity
from domain.products.services import ProductService


@dataclass(frozen=True)
class CreateProductCommand(BaseCommand):
    product: ProductEntity


@dataclass(frozen=True)
class CreateProductCommandHandler(
    BaseCommandHandler[CreateProductCommand, ProductEntity],
):
    product_service: ProductService
    portfolio_service: PortfolioService

    async def handle(self, command: CreateProductCommand) -> ProductEntity:
        if command.product.portfolio_ids:
            for portfolio_id in command.product.portfolio_ids:
                await self.portfolio_service.check_exists(portfolio_id)

        return await self.product_service.create(command.product)
