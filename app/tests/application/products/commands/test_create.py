import pytest
from faker import Faker

from application.mediator import Mediator
from application.products.commands import CreateProductCommand
from application.products.queries import GetProductByIdQuery
from domain.products.entities import ProductEntity
from domain.products.exceptions.products import ProductAlreadyExistsException
from domain.products.value_objects import NameValueObject


@pytest.mark.asyncio
async def test_create_product_command_success(
    mediator: Mediator,
    valid_product_entity: ProductEntity,
):
    command = CreateProductCommand(product=valid_product_entity)
    result, *_ = await mediator.handle_command(command)

    product: ProductEntity = result

    assert product is not None
    assert product.category.as_generic_type() == valid_product_entity.category.as_generic_type()
    assert product.name.as_generic_type() == valid_product_entity.name.as_generic_type()
    assert product.slug.as_generic_type() == valid_product_entity.slug.as_generic_type()
    assert product.description.as_generic_type() == valid_product_entity.description.as_generic_type()
    assert product.preview_image_url.as_generic_type() == valid_product_entity.preview_image_url.as_generic_type()
    assert product.preview_image_alt.as_generic_type() == valid_product_entity.preview_image_alt.as_generic_type()
    assert product.oid is not None

    retrieved_product = await mediator.handle_query(
        GetProductByIdQuery(product_id=product.oid),
    )

    assert retrieved_product.oid == product.oid
    assert retrieved_product.slug.as_generic_type() == valid_product_entity.slug.as_generic_type()


@pytest.mark.asyncio
async def test_create_product_command_duplicate_slug(
    mediator: Mediator,
    valid_product_entity: ProductEntity,
    faker: Faker,
):
    command = CreateProductCommand(product=valid_product_entity)
    await mediator.handle_command(command)

    duplicate_product = ProductEntity(
        category=valid_product_entity.category,
        name=NameValueObject(value=faker.sentence(nb_words=5)),
        slug=valid_product_entity.slug,
        description=valid_product_entity.description,
        preview_image_url=valid_product_entity.preview_image_url,
        preview_image_alt=valid_product_entity.preview_image_alt,
    )

    with pytest.raises(ProductAlreadyExistsException) as exc_info:
        await mediator.handle_command(CreateProductCommand(product=duplicate_product))

    assert exc_info.value.slug == valid_product_entity.slug.as_generic_type()
