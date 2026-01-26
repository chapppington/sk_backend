from uuid import uuid4

import pytest
from faker import Faker

from application.mediator import Mediator
from application.products.commands import (
    CreateProductCommand,
    UpdateProductCommand,
)
from application.products.queries import GetProductByIdQuery
from domain.products.entities import ProductEntity
from domain.products.exceptions.products import (
    ProductAlreadyExistsException,
    ProductNotFoundException,
)


@pytest.mark.asyncio
async def test_update_product_command_success(mediator: Mediator, valid_product_data: dict):
    create_result, *_ = await mediator.handle_command(
        CreateProductCommand(**valid_product_data),
    )
    created_product: ProductEntity = create_result

    update_data = valid_product_data.copy()
    update_data["product_id"] = created_product.oid
    update_data["name"] = "Updated Product Name"

    update_result, *_ = await mediator.handle_command(
        UpdateProductCommand(**update_data),
    )

    updated_product: ProductEntity = update_result

    assert updated_product.oid == created_product.oid
    assert updated_product.name.as_generic_type() == "Updated Product Name"
    assert updated_product.slug.as_generic_type() == update_data["slug"]

    retrieved_product = await mediator.handle_query(
        GetProductByIdQuery(product_id=created_product.oid),
    )

    assert retrieved_product.name.as_generic_type() == "Updated Product Name"


@pytest.mark.asyncio
async def test_update_product_command_not_found(mediator: Mediator, valid_product_data: dict):
    update_data = valid_product_data.copy()
    update_data["product_id"] = uuid4()

    with pytest.raises(ProductNotFoundException) as exc_info:
        await mediator.handle_command(
            UpdateProductCommand(**update_data),
        )

    assert exc_info.value.product_id == update_data["product_id"]


@pytest.mark.asyncio
async def test_update_product_command_duplicate_slug(
    mediator: Mediator,
    valid_product_data: dict,
    faker: Faker,
):
    data1 = valid_product_data.copy()
    data2 = valid_product_data.copy()
    data2["slug"] = faker.slug()

    create_result1, *_ = await mediator.handle_command(
        CreateProductCommand(**data1),
    )
    created_product1: ProductEntity = create_result1

    await mediator.handle_command(
        CreateProductCommand(**data2),
    )

    update_data = valid_product_data.copy()
    update_data["product_id"] = created_product1.oid
    update_data["slug"] = data2["slug"]

    with pytest.raises(ProductAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            UpdateProductCommand(**update_data),
        )

    assert exc_info.value.slug == data2["slug"]
