from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.products.services import ProductService


@dataclass(frozen=True)
class DeleteProductCommand(BaseCommand):
    product_id: UUID


@dataclass(frozen=True)
class DeleteProductCommandHandler(
    BaseCommandHandler[DeleteProductCommand, None],
):
    product_service: ProductService

    async def handle(self, command: DeleteProductCommand) -> None:
        await self.product_service.delete(command.product_id)
