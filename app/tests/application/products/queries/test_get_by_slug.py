import pytest
from faker import Faker

from application.mediator import Mediator
from application.products.commands import CreateProductCommand
from application.products.queries import GetProductBySlugQuery
from domain.products.entities.products import ProductEntity
from domain.products.exceptions.products import ProductNotFoundBySlugException


@pytest.mark.asyncio
async def test_get_product_by_slug_success(
    mediator: Mediator,
    valid_product_entity: ProductEntity,
):
    slug = valid_product_entity.slug.as_generic_type()

    await mediator.handle_command(
        CreateProductCommand(product=valid_product_entity),
    )

    retrieved_product = await mediator.handle_query(
        GetProductBySlugQuery(slug=slug),
    )

    assert retrieved_product.slug.as_generic_type() == slug
    assert retrieved_product.name.as_generic_type() == valid_product_entity.name.as_generic_type()


@pytest.mark.asyncio
async def test_get_product_by_slug_not_found(
    mediator: Mediator,
    faker: Faker,
):
    non_existent_slug = faker.slug()

    with pytest.raises(ProductNotFoundBySlugException) as exc_info:
        await mediator.handle_query(
            GetProductBySlugQuery(slug=non_existent_slug),
        )

    assert exc_info.value.slug == non_existent_slug
