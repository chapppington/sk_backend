import pytest
from faker import Faker

from application.mediator import Mediator
from application.products.commands import CreateProductCommand
from application.products.queries import GetProductByIdQuery
from domain.products.entities import ProductEntity
from domain.products.exceptions.products import (
    CategoryInvalidException,
    DescriptionEmptyException,
    NameEmptyException,
    NameTooLongException,
    PreviewImageUrlInvalidException,
    ProductAlreadyExistsException,
    SlugEmptyException,
    SlugInvalidException,
)


@pytest.mark.asyncio
async def test_create_product_command_success(
    mediator: Mediator,
    valid_product_data: dict,
):
    result, *_ = await mediator.handle_command(
        CreateProductCommand(**valid_product_data),
    )

    product: ProductEntity = result

    assert product is not None
    assert product.category.as_generic_type() == valid_product_data["category"]
    assert product.name.as_generic_type() == valid_product_data["name"]
    assert product.slug.as_generic_type() == valid_product_data["slug"]
    assert product.description.as_generic_type() == valid_product_data["description"]
    assert product.preview_image_url.as_generic_type() == valid_product_data["preview_image_url"]
    assert product.preview_image_alt.as_generic_type() == valid_product_data["preview_image_alt"]
    assert product.oid is not None

    retrieved_product = await mediator.handle_query(
        GetProductByIdQuery(product_id=product.oid),
    )

    assert retrieved_product.oid == product.oid
    assert retrieved_product.slug.as_generic_type() == valid_product_data["slug"]


@pytest.mark.asyncio
async def test_create_product_command_invalid_category(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["category"] = "InvalidCategory"

    with pytest.raises(CategoryInvalidException) as exc_info:
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )

    assert exc_info.value.category == "InvalidCategory"


@pytest.mark.asyncio
async def test_create_product_command_empty_name(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["name"] = ""

    with pytest.raises(NameEmptyException):
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )


@pytest.mark.asyncio
async def test_create_product_command_name_too_long(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["name"] = "a" * 256

    with pytest.raises(NameTooLongException) as exc_info:
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )

    assert exc_info.value.name_length == 256
    assert exc_info.value.max_length == 255


@pytest.mark.asyncio
async def test_create_product_command_empty_slug(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["slug"] = ""

    with pytest.raises(SlugEmptyException):
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )


@pytest.mark.asyncio
async def test_create_product_command_invalid_slug(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["slug"] = "invalid slug with spaces"

    with pytest.raises(SlugInvalidException) as exc_info:
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )

    assert exc_info.value.slug == "invalid slug with spaces"


@pytest.mark.asyncio
async def test_create_product_command_empty_description(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["description"] = ""

    with pytest.raises(DescriptionEmptyException):
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )


@pytest.mark.asyncio
async def test_create_product_command_invalid_preview_image_url(
    mediator: Mediator,
    valid_product_data: dict,
):
    valid_product_data["preview_image_url"] = "not-a-valid-url"

    with pytest.raises(PreviewImageUrlInvalidException) as exc_info:
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )

    assert exc_info.value.url == "not-a-valid-url"


@pytest.mark.asyncio
async def test_create_product_command_duplicate_slug(
    mediator: Mediator,
    valid_product_data: dict,
    faker: Faker,
):
    slug = valid_product_data["slug"]

    await mediator.handle_command(
        CreateProductCommand(**valid_product_data),
    )

    valid_product_data["name"] = faker.sentence(nb_words=5)

    with pytest.raises(ProductAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            CreateProductCommand(**valid_product_data),
        )

    assert exc_info.value.slug == slug
