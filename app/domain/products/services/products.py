from collections.abc import AsyncIterable
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.products.entities import ProductEntity
from domain.products.exceptions import (
    ProductAlreadyExistsException,
    ProductNotFoundBySlugException,
    ProductNotFoundException,
)
from domain.products.interfaces.repository import BaseProductRepository


@dataclass
class ProductService:
    product_repository: BaseProductRepository

    async def create(
        self,
        product: ProductEntity,
    ) -> ProductEntity:
        slug = product.slug.as_generic_type()
        existing_product = await self.product_repository.get_by_slug(slug)

        if existing_product:
            raise ProductAlreadyExistsException(slug=slug)

        await self.product_repository.add(product)

        return product

    async def get_by_id(
        self,
        product_id: UUID,
    ) -> ProductEntity:
        product = await self.product_repository.get_by_id(product_id)

        if not product:
            raise ProductNotFoundException(product_id=product_id)

        return product

    async def get_by_slug(
        self,
        slug: str,
    ) -> ProductEntity:
        product = await self.product_repository.get_by_slug(slug)

        if not product:
            raise ProductNotFoundBySlugException(slug=slug)

        return product

    async def update(
        self,
        product: ProductEntity,
    ) -> ProductEntity:
        existing_product = await self.product_repository.get_by_id(product.oid)

        if not existing_product:
            raise ProductNotFoundException(product_id=product.oid)

        current_slug = existing_product.slug.as_generic_type()
        new_slug = product.slug.as_generic_type()

        if new_slug != current_slug:
            product_with_slug = await self.product_repository.get_by_slug(new_slug)

            if product_with_slug:
                raise ProductAlreadyExistsException(slug=new_slug)

        await self.product_repository.update(product)

        return product

    async def delete(
        self,
        product_id: UUID,
    ) -> None:
        await self.get_by_id(product_id)
        await self.product_repository.delete(product_id)

    def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_shown: Optional[bool] = None,
    ) -> AsyncIterable[ProductEntity]:
        return self.product_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
            category=category,
            is_shown=is_shown,
        )

    async def count_many(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_shown: Optional[bool] = None,
    ) -> int:
        return await self.product_repository.count_many(
            search=search,
            category=category,
            is_shown=is_shown,
        )
