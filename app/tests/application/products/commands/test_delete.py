from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.products.commands import (
    CreateProductCommand,
    DeleteProductCommand,
)
from application.products.queries import GetProductByIdQuery
from domain.products.entities import ProductEntity
from domain.products.exceptions.products import ProductNotFoundException


@pytest.mark.asyncio
async def test_delete_product_command_success(
    mediator: Mediator,
    valid_product_data: dict,
):
    create_result, *_ = await mediator.handle_command(
        CreateProductCommand(**valid_product_data),
    )
    created_product: ProductEntity = create_result

    await mediator.handle_command(
        DeleteProductCommand(product_id=created_product.oid),
    )

    with pytest.raises(ProductNotFoundException):
        await mediator.handle_query(
            GetProductByIdQuery(product_id=created_product.oid),
        )


@pytest.mark.asyncio
async def test_delete_product_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(ProductNotFoundException) as exc_info:
        await mediator.handle_command(
            DeleteProductCommand(product_id=non_existent_id),
        )

    assert exc_info.value.product_id == non_existent_id
