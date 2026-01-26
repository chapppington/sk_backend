from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.products.entities import ProductEntity
from domain.products.services import ProductService


@dataclass(frozen=True)
class GetProductByIdQuery(BaseQuery):
    product_id: UUID


@dataclass(frozen=True)
class GetProductByIdQueryHandler(
    BaseQueryHandler[GetProductByIdQuery, ProductEntity],
):
    product_service: ProductService

    async def handle(
        self,
        query: GetProductByIdQuery,
    ) -> ProductEntity:
        return await self.product_service.get_by_id(
            product_id=query.product_id,
        )
