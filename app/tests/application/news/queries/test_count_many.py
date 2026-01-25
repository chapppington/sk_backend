import pytest

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import CountManyNewsQuery


@pytest.mark.asyncio
async def test_count_many_news_query_success(
    mediator: Mediator,
    valid_news_data_with_category,
):
    for _ in range(3):
        data = valid_news_data_with_category()
        await mediator.handle_command(
            CreateNewsCommand(**data),
        )

    count = await mediator.handle_query(
        CountManyNewsQuery(),
    )

    assert count == 3


@pytest.mark.asyncio
async def test_count_many_news_query_with_category(
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

    count = await mediator.handle_query(
        CountManyNewsQuery(category="События"),
    )

    assert count == 3


@pytest.mark.asyncio
async def test_count_many_news_query_with_search(
    mediator: Mediator,
    valid_news_data_with_category,
):
    data1 = valid_news_data_with_category()
    data1["title"] = "Python tutorial"
    await mediator.handle_command(
        CreateNewsCommand(**data1),
    )

    data2 = valid_news_data_with_category()
    data2["title"] = "JavaScript guide"
    await mediator.handle_command(
        CreateNewsCommand(**data2),
    )

    count = await mediator.handle_query(
        CountManyNewsQuery(search="Python"),
    )

    assert count == 1
