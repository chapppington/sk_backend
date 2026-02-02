from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
    replace,
)
from datetime import datetime
from uuid import UUID

from domain.products.entities import ProductEntity
from domain.products.interfaces.repository import BaseProductRepository


@dataclass
class DummyInMemoryProductRepository(BaseProductRepository):
    _saved_products: list[ProductEntity] = field(default_factory=list, kw_only=True)

    async def add(self, product: ProductEntity) -> ProductEntity:
        self._saved_products.append(product)
        return product

    async def get_by_id(self, product_id: UUID) -> ProductEntity | None:
        try:
            return next(product for product in self._saved_products if product.oid == product_id)
        except StopIteration:
            return None

    async def get_by_slug(self, slug: str) -> ProductEntity | None:
        try:
            return next(product for product in self._saved_products if product.slug.as_generic_type() == slug)
        except StopIteration:
            return None

    async def update(self, product: ProductEntity) -> None:
        for i, saved_product in enumerate(self._saved_products):
            if saved_product.oid == product.oid:
                self._saved_products[i] = product
                return
        raise ValueError(f"Product with id {product.oid} not found")

    async def update_order(self, product_id: UUID, order: int) -> None:
        for i, saved_product in enumerate(self._saved_products):
            if saved_product.oid == product_id:
                self._saved_products[i] = replace(
                    saved_product,
                    order=order,
                    updated_at=datetime.now(),
                )
                return
        raise ValueError(f"Product with id {product_id} not found")

    async def delete(self, product_id: UUID) -> None:
        self._saved_products = [product for product in self._saved_products if product.oid != product_id]

    def _build_find_query(
        self,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> list[ProductEntity]:
        filtered_products = self._saved_products.copy()

        if category:
            filtered_products = [
                product for product in filtered_products if product.category.as_generic_type() == category
            ]

        if is_shown is not None:
            filtered_products = [product for product in filtered_products if product.is_shown == is_shown]

        if search:
            search_lower = search.lower()
            filtered_products = [
                product
                for product in filtered_products
                if (
                    search_lower in product.name.as_generic_type().lower()
                    or search_lower in product.description.as_generic_type().lower()
                    or search_lower in product.category.as_generic_type().lower()
                )
            ]

        return filtered_products

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> AsyncIterable[ProductEntity]:
        filtered_products = self._build_find_query(search, category, is_shown)

        reverse = sort_order == -1

        if sort_field == "order":
            filtered_products.sort(key=lambda x: x.order, reverse=reverse)
        elif sort_field == "created_at":
            filtered_products.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "name":
            filtered_products.sort(key=lambda x: x.name.as_generic_type(), reverse=reverse)
        else:
            filtered_products.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_products = filtered_products[offset : offset + limit]

        for product in paginated_products:
            yield product

    async def count_many(
        self,
        search: str | None = None,
        category: str | None = None,
        is_shown: bool | None = None,
    ) -> int:
        filtered_products = self._build_find_query(search, category, is_shown)
        return len(filtered_products)
