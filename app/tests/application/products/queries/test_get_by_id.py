from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.products.commands import CreateProductCommand
from application.products.queries import GetProductByIdQuery
from domain.products.entities import ProductEntity
from domain.products.exceptions.products import ProductNotFoundException


@pytest.mark.asyncio
async def test_get_product_by_id_success(
    mediator: Mediator,
    valid_product_entity: ProductEntity,
):
    create_result, *_ = await mediator.handle_command(
        CreateProductCommand(product=valid_product_entity),
    )
    created_product: ProductEntity = create_result

    retrieved_product = await mediator.handle_query(
        GetProductByIdQuery(product_id=created_product.oid),
    )

    assert retrieved_product.oid == created_product.oid
    assert retrieved_product.category.as_generic_type() == valid_product_entity.category.as_generic_type()
    assert retrieved_product.name.as_generic_type() == valid_product_entity.name.as_generic_type()
    assert retrieved_product.slug.as_generic_type() == valid_product_entity.slug.as_generic_type()


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(ProductNotFoundException) as exc_info:
        await mediator.handle_query(
            GetProductByIdQuery(product_id=non_existent_id),
        )

    assert exc_info.value.product_id == non_existent_id
