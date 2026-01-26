import pytest

from application.mediator import Mediator
from application.products.commands import CreateProductCommand
from application.products.queries import GetProductListQuery
from domain.products.entities import ProductEntity


@pytest.mark.asyncio
async def test_get_product_list_query_success(
    mediator: Mediator,
    valid_product_data_with_category,
):
    for _ in range(5):
        data = valid_product_data_with_category("Трансформаторные подстанции")
        await mediator.handle_command(
            CreateProductCommand(**data),
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
    valid_product_data_with_category,
):
    for _ in range(5):
        data = valid_product_data_with_category()
        await mediator.handle_command(
            CreateProductCommand(**data),
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
    valid_product_data_with_category,
):
    for _ in range(3):
        data = valid_product_data_with_category("Трансформаторные подстанции")
        await mediator.handle_command(
            CreateProductCommand(**data),
        )

    for _ in range(2):
        data = valid_product_data_with_category("Распределительные устройства среднего напряжения 6(10) кВ")
        await mediator.handle_command(
            CreateProductCommand(**data),
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
    valid_product_data_with_category,
):
    data1 = valid_product_data_with_category()
    data1["name"] = "Python Transformer"
    await mediator.handle_command(
        CreateProductCommand(**data1),
    )

    data2 = valid_product_data_with_category()
    data2["name"] = "JavaScript Switchgear"
    await mediator.handle_command(
        CreateProductCommand(**data2),
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
    valid_product_data_with_category,
):
    data1 = valid_product_data_with_category()
    data1["name"] = "First Product"
    await mediator.handle_command(
        CreateProductCommand(**data1),
    )

    data2 = valid_product_data_with_category()
    data2["name"] = "Second Product"
    await mediator.handle_command(
        CreateProductCommand(**data2),
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
    valid_product_data_with_category,
):
    data1 = valid_product_data_with_category()
    data1["is_shown"] = True
    await mediator.handle_command(
        CreateProductCommand(**data1),
    )

    data2 = valid_product_data_with_category()
    data2["is_shown"] = False
    await mediator.handle_command(
        CreateProductCommand(**data2),
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
    valid_product_data_with_category,
):
    for _ in range(3):
        data = valid_product_data_with_category()
        await mediator.handle_command(
            CreateProductCommand(**data),
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
    valid_product_data_with_category,
):
    for _ in range(3):
        data = valid_product_data_with_category("Трансформаторные подстанции")
        await mediator.handle_command(
            CreateProductCommand(**data),
        )

    for _ in range(2):
        data = valid_product_data_with_category("Распределительные устройства среднего напряжения 6(10) кВ")
        await mediator.handle_command(
            CreateProductCommand(**data),
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
    valid_product_data_with_category,
):
    data1 = valid_product_data_with_category()
    data1["name"] = "Python Transformer"
    await mediator.handle_command(
        CreateProductCommand(**data1),
    )

    data2 = valid_product_data_with_category()
    data2["name"] = "JavaScript Switchgear"
    await mediator.handle_command(
        CreateProductCommand(**data2),
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
