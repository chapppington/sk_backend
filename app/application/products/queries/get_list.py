import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.products.entities import ProductEntity
from domain.products.services import ProductService


@dataclass(frozen=True)
class GetProductListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    category: Optional[str] = None
    is_shown: Optional[bool] = None


@dataclass(frozen=True)
class GetProductListQueryHandler(
    BaseQueryHandler[GetProductListQuery, tuple[list[ProductEntity], int]],
):
    product_service: ProductService

    async def handle(
        self,
        query: GetProductListQuery,
    ) -> tuple[list[ProductEntity], int]:
        products_task = asyncio.create_task(
            self.product_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                search=query.search,
                category=query.category,
                is_shown=query.is_shown,
            ),
        )
        count_task = asyncio.create_task(
            self.product_service.count_many(
                search=query.search,
                category=query.category,
                is_shown=query.is_shown,
            ),
        )

        return await products_task, await count_task
