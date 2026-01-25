import pytest

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import FindManyNewsQuery
from domain.news.entities import NewsEntity


@pytest.mark.asyncio
async def test_find_many_news_query_success(
    mediator: Mediator,
    valid_news_data_with_category,
):
    for _ in range(5):
        data = valid_news_data_with_category("События")
        await mediator.handle_command(
            CreateNewsCommand(**data),
        )

    news_list = await mediator.handle_query(
        FindManyNewsQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(news_list) == 5
    assert all(isinstance(news, NewsEntity) for news in news_list)


@pytest.mark.asyncio
async def test_find_many_news_query_with_pagination(
    mediator: Mediator,
    valid_news_data_with_category,
):
    for _ in range(5):
        data = valid_news_data_with_category()
        await mediator.handle_command(
            CreateNewsCommand(**data),
        )

    news_list = await mediator.handle_query(
        FindManyNewsQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(news_list) == 2

    news_list = await mediator.handle_query(
        FindManyNewsQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(news_list) == 2


@pytest.mark.asyncio
async def test_find_many_news_query_with_category_filter(
    mediator: Mediator,
    valid_news_data_with_category,
):
    for _ in range(3):
        data = valid_news_data_with_category("События")
        await mediator.handle_command(
            CreateNewsCommand(**data),
        )

    for _ in range(2):
        data = valid_news_data_with_category("Полезное")
        await mediator.handle_command(
            CreateNewsCommand(**data),
        )

    news_list = await mediator.handle_query(
        FindManyNewsQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="События",
        ),
    )

    assert len(news_list) == 3
    assert all(news.category.as_generic_type() == "События" for news in news_list)


@pytest.mark.asyncio
async def test_find_many_news_query_with_search(
    mediator: Mediator,
    valid_news_data_with_category,
):
    data1 = valid_news_data_with_category()
    data1["title"] = "Python programming"
    await mediator.handle_command(
        CreateNewsCommand(**data1),
    )

    data2 = valid_news_data_with_category()
    data2["title"] = "JavaScript development"
    await mediator.handle_command(
        CreateNewsCommand(**data2),
    )

    news_list = await mediator.handle_query(
        FindManyNewsQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(news_list) == 1
    assert "Python" in news_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_find_many_news_query_with_sorting(
    mediator: Mediator,
    valid_news_data_with_category,
):
    data1 = valid_news_data_with_category()
    data1["title"] = "First News"
    await mediator.handle_command(
        CreateNewsCommand(**data1),
    )

    data2 = valid_news_data_with_category()
    data2["title"] = "Second News"
    await mediator.handle_command(
        CreateNewsCommand(**data2),
    )

    news_list = await mediator.handle_query(
        FindManyNewsQuery(
            sort_field="title",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(news_list) == 2
    assert news_list[0].title.as_generic_type() < news_list[1].title.as_generic_type()
