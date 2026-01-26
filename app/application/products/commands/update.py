from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.services.portfolios import PortfolioService
from domain.products.entities import ProductEntity
from domain.products.services import ProductService


@dataclass(frozen=True)
class UpdateProductCommand(BaseCommand):
    product_id: UUID
    product: ProductEntity


@dataclass(frozen=True)
class UpdateProductCommandHandler(
    BaseCommandHandler[UpdateProductCommand, ProductEntity],
):
    product_service: ProductService
    portfolio_service: PortfolioService

    async def handle(self, command: UpdateProductCommand) -> ProductEntity:
        existing_product = await self.product_service.get_by_id(command.product_id)

        if command.product.portfolio_ids:
            for portfolio_id in command.product.portfolio_ids:
                await self.portfolio_service.check_exists(portfolio_id)

        updated_product = ProductEntity(
            oid=existing_product.oid,
            created_at=existing_product.created_at,
            category=command.product.category,
            name=command.product.name,
            slug=command.product.slug,
            description=command.product.description,
            preview_image_url=command.product.preview_image_url,
            preview_image_alt=command.product.preview_image_alt,
            important_characteristics=command.product.important_characteristics,
            advantages=command.product.advantages,
            simple_description=command.product.simple_description,
            detailed_description=command.product.detailed_description,
            documentation=command.product.documentation,
            order=command.product.order,
            is_shown=command.product.is_shown,
            show_advantages=command.product.show_advantages,
            portfolio_ids=command.product.portfolio_ids,
        )

        return await self.product_service.update(updated_product)
