from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.products.entities import ProductEntity
from domain.products.services import ProductService


@dataclass(frozen=True)
class GetProductBySlugQuery(BaseQuery):
    slug: str


@dataclass(frozen=True)
class GetProductBySlugQueryHandler(
    BaseQueryHandler[GetProductBySlugQuery, ProductEntity],
):
    product_service: ProductService

    async def handle(
        self,
        query: GetProductBySlugQuery,
    ) -> ProductEntity:
        return await self.product_service.get_by_slug(
            slug=query.slug,
        )
