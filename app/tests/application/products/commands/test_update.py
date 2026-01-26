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
from domain.products.value_objects import (
    NameValueObject,
    SlugValueObject,
)


@pytest.mark.asyncio
async def test_update_product_command_success(mediator: Mediator, valid_product_entity: ProductEntity):
    create_command = CreateProductCommand(product=valid_product_entity)
    create_result, *_ = await mediator.handle_command(create_command)
    created_product: ProductEntity = create_result

    updated_product = ProductEntity(
        category=created_product.category,
        name=NameValueObject(value="Updated Product Name"),
        slug=created_product.slug,
        description=created_product.description,
        preview_image_url=created_product.preview_image_url,
        preview_image_alt=created_product.preview_image_alt,
        important_characteristics=created_product.important_characteristics,
        advantages=created_product.advantages,
        simple_description=created_product.simple_description,
        detailed_description=created_product.detailed_description,
        documentation=created_product.documentation,
        order=created_product.order,
        is_shown=created_product.is_shown,
        show_advantages=created_product.show_advantages,
        portfolio_ids=created_product.portfolio_ids,
    )

    update_command = UpdateProductCommand(product_id=created_product.oid, product=updated_product)
    update_result, *_ = await mediator.handle_command(update_command)

    updated: ProductEntity = update_result

    assert updated.oid == created_product.oid
    assert updated.name.as_generic_type() == "Updated Product Name"
    assert updated.slug.as_generic_type() == created_product.slug.as_generic_type()

    retrieved_product = await mediator.handle_query(
        GetProductByIdQuery(product_id=created_product.oid),
    )

    assert retrieved_product.name.as_generic_type() == "Updated Product Name"


@pytest.mark.asyncio
async def test_update_product_command_not_found(
    mediator: Mediator,
    valid_product_entity: ProductEntity,
):
    non_existent_id = uuid4()
    update_command = UpdateProductCommand(product_id=non_existent_id, product=valid_product_entity)

    with pytest.raises(ProductNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.product_id == non_existent_id


@pytest.mark.asyncio
async def test_update_product_command_duplicate_slug(
    mediator: Mediator,
    valid_product_entity: ProductEntity,
    faker: Faker,
):
    product1 = ProductEntity(
        category=valid_product_entity.category,
        name=valid_product_entity.name,
        slug=valid_product_entity.slug,
        description=valid_product_entity.description,
        preview_image_url=valid_product_entity.preview_image_url,
        preview_image_alt=valid_product_entity.preview_image_alt,
    )

    product2 = ProductEntity(
        category=valid_product_entity.category,
        name=NameValueObject(value=faker.sentence(nb_words=5)),
        slug=SlugValueObject(value=faker.slug()),
        description=valid_product_entity.description,
        preview_image_url=valid_product_entity.preview_image_url,
        preview_image_alt=valid_product_entity.preview_image_alt,
    )

    create_result1, *_ = await mediator.handle_command(CreateProductCommand(product=product1))
    created_product1: ProductEntity = create_result1

    create_result2, *_ = await mediator.handle_command(CreateProductCommand(product=product2))
    created_product2: ProductEntity = create_result2

    updated_product = ProductEntity(
        category=created_product1.category,
        name=created_product1.name,
        slug=created_product2.slug,
        description=created_product1.description,
        preview_image_url=created_product1.preview_image_url,
        preview_image_alt=created_product1.preview_image_alt,
        important_characteristics=created_product1.important_characteristics,
        advantages=created_product1.advantages,
        simple_description=created_product1.simple_description,
        detailed_description=created_product1.detailed_description,
        documentation=created_product1.documentation,
        order=created_product1.order,
        is_shown=created_product1.is_shown,
        show_advantages=created_product1.show_advantages,
        portfolio_ids=created_product1.portfolio_ids,
    )

    update_command = UpdateProductCommand(product_id=created_product1.oid, product=updated_product)

    with pytest.raises(ProductAlreadyExistsException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.slug == created_product2.slug.as_generic_type()
