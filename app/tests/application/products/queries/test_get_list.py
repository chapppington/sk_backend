import pytest
from faker import Faker

from application.mediator import Mediator
from application.products.commands import CreateProductCommand
from application.products.queries import GetProductListQuery
from domain.products.entities import ProductEntity
from domain.products.value_objects import NameValueObject


@pytest.mark.asyncio
async def test_get_product_list_query_success(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    for _ in range(5):
        product = valid_product_entity_with_category("Трансформаторные подстанции")
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(product_list) == 5
    assert total == 5
    assert all(isinstance(product, ProductEntity) for product in product_list)


@pytest.mark.asyncio
async def test_get_product_list_query_with_pagination(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    for _ in range(5):
        product = valid_product_entity_with_category()
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(product_list) == 2
    assert total == 5

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(product_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_product_list_query_with_category_filter(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    for _ in range(3):
        product = valid_product_entity_with_category("Трансформаторные подстанции")
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    for _ in range(2):
        product = valid_product_entity_with_category("Распределительные устройства среднего напряжения 6(10) кВ")
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="Трансформаторные подстанции",
        ),
    )

    assert len(product_list) == 3
    assert total == 3
    assert all(product.category.as_generic_type() == "Трансформаторные подстанции" for product in product_list)


@pytest.mark.asyncio
async def test_get_product_list_query_with_search(
    mediator: Mediator,
    valid_product_entity_with_category,
    faker: Faker,
):
    product1 = valid_product_entity_with_category()
    product1 = ProductEntity(
        category=product1.category,
        name=NameValueObject(value="Python Transformer"),
        slug=product1.slug,
        description=product1.description,
        preview_image_url=product1.preview_image_url,
        preview_image_alt=product1.preview_image_alt,
        important_characteristics=product1.important_characteristics,
        advantages=product1.advantages,
        simple_description=product1.simple_description,
        detailed_description=product1.detailed_description,
        documentation=product1.documentation,
        order=product1.order,
        is_shown=product1.is_shown,
        show_advantages=product1.show_advantages,
        portfolio_ids=product1.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product1),
    )

    product2 = valid_product_entity_with_category()
    product2 = ProductEntity(
        category=product2.category,
        name=NameValueObject(value="JavaScript Switchgear"),
        slug=product2.slug,
        description=product2.description,
        preview_image_url=product2.preview_image_url,
        preview_image_alt=product2.preview_image_alt,
        important_characteristics=product2.important_characteristics,
        advantages=product2.advantages,
        simple_description=product2.simple_description,
        detailed_description=product2.detailed_description,
        documentation=product2.documentation,
        order=product2.order,
        is_shown=product2.is_shown,
        show_advantages=product2.show_advantages,
        portfolio_ids=product2.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product2),
    )

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(product_list) == 1
    assert total == 1
    assert "Python" in product_list[0].name.as_generic_type()


@pytest.mark.asyncio
async def test_get_product_list_query_with_sorting(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    product1 = valid_product_entity_with_category()
    product1 = ProductEntity(
        category=product1.category,
        name=NameValueObject(value="First Product"),
        slug=product1.slug,
        description=product1.description,
        preview_image_url=product1.preview_image_url,
        preview_image_alt=product1.preview_image_alt,
        important_characteristics=product1.important_characteristics,
        advantages=product1.advantages,
        simple_description=product1.simple_description,
        detailed_description=product1.detailed_description,
        documentation=product1.documentation,
        order=product1.order,
        is_shown=product1.is_shown,
        show_advantages=product1.show_advantages,
        portfolio_ids=product1.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product1),
    )

    product2 = valid_product_entity_with_category()
    product2 = ProductEntity(
        category=product2.category,
        name=NameValueObject(value="Second Product"),
        slug=product2.slug,
        description=product2.description,
        preview_image_url=product2.preview_image_url,
        preview_image_alt=product2.preview_image_alt,
        important_characteristics=product2.important_characteristics,
        advantages=product2.advantages,
        simple_description=product2.simple_description,
        detailed_description=product2.detailed_description,
        documentation=product2.documentation,
        order=product2.order,
        is_shown=product2.is_shown,
        show_advantages=product2.show_advantages,
        portfolio_ids=product2.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product2),
    )

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="name",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(product_list) == 2
    assert total == 2
    assert product_list[0].name.as_generic_type() < product_list[1].name.as_generic_type()


@pytest.mark.asyncio
async def test_get_product_list_query_with_is_shown_filter(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    product1 = valid_product_entity_with_category()
    product1 = ProductEntity(
        category=product1.category,
        name=product1.name,
        slug=product1.slug,
        description=product1.description,
        preview_image_url=product1.preview_image_url,
        preview_image_alt=product1.preview_image_alt,
        important_characteristics=product1.important_characteristics,
        advantages=product1.advantages,
        simple_description=product1.simple_description,
        detailed_description=product1.detailed_description,
        documentation=product1.documentation,
        order=product1.order,
        is_shown=True,
        show_advantages=product1.show_advantages,
        portfolio_ids=product1.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product1),
    )

    product2 = valid_product_entity_with_category()
    product2 = ProductEntity(
        category=product2.category,
        name=product2.name,
        slug=product2.slug,
        description=product2.description,
        preview_image_url=product2.preview_image_url,
        preview_image_alt=product2.preview_image_alt,
        important_characteristics=product2.important_characteristics,
        advantages=product2.advantages,
        simple_description=product2.simple_description,
        detailed_description=product2.detailed_description,
        documentation=product2.documentation,
        order=product2.order,
        is_shown=False,
        show_advantages=product2.show_advantages,
        portfolio_ids=product2.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product2),
    )

    product_list, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            is_shown=True,
        ),
    )

    assert len(product_list) == 1
    assert total == 1
    assert product_list[0].is_shown is True


@pytest.mark.asyncio
async def test_get_product_list_query_count_only(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    for _ in range(3):
        product = valid_product_entity_with_category()
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    _, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_product_list_query_count_with_category(
    mediator: Mediator,
    valid_product_entity_with_category,
):
    for _ in range(3):
        product = valid_product_entity_with_category("Трансформаторные подстанции")
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    for _ in range(2):
        product = valid_product_entity_with_category("Распределительные устройства среднего напряжения 6(10) кВ")
        await mediator.handle_command(
            CreateProductCommand(product=product),
        )

    _, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="Трансформаторные подстанции",
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_product_list_query_count_with_search(
    mediator: Mediator,
    valid_product_entity_with_category,
    faker: Faker,
):
    product1 = valid_product_entity_with_category()
    product1 = ProductEntity(
        category=product1.category,
        name=NameValueObject(value="Python Transformer"),
        slug=product1.slug,
        description=product1.description,
        preview_image_url=product1.preview_image_url,
        preview_image_alt=product1.preview_image_alt,
        important_characteristics=product1.important_characteristics,
        advantages=product1.advantages,
        simple_description=product1.simple_description,
        detailed_description=product1.detailed_description,
        documentation=product1.documentation,
        order=product1.order,
        is_shown=product1.is_shown,
        show_advantages=product1.show_advantages,
        portfolio_ids=product1.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product1),
    )

    product2 = valid_product_entity_with_category()
    product2 = ProductEntity(
        category=product2.category,
        name=NameValueObject(value="JavaScript Switchgear"),
        slug=product2.slug,
        description=product2.description,
        preview_image_url=product2.preview_image_url,
        preview_image_alt=product2.preview_image_alt,
        important_characteristics=product2.important_characteristics,
        advantages=product2.advantages,
        simple_description=product2.simple_description,
        detailed_description=product2.detailed_description,
        documentation=product2.documentation,
        order=product2.order,
        is_shown=product2.is_shown,
        show_advantages=product2.show_advantages,
        portfolio_ids=product2.portfolio_ids,
    )
    await mediator.handle_command(
        CreateProductCommand(product=product2),
    )

    _, total = await mediator.handle_query(
        GetProductListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert total == 1
