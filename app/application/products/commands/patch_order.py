from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.products.entities import ProductEntity
from domain.products.services import ProductService


@dataclass(frozen=True)
class PatchProductOrderCommand(BaseCommand):
    product_id: UUID
    order: int


@dataclass(frozen=True)
class PatchProductOrderCommandHandler(
    BaseCommandHandler[PatchProductOrderCommand, ProductEntity],
):
    product_service: ProductService

    async def handle(self, command: PatchProductOrderCommand) -> ProductEntity:
        return await self.product_service.update_order(
            product_id=command.product_id,
            order=command.order,
        )
