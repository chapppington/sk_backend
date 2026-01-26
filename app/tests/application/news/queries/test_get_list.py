import pytest
from faker import Faker

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import GetNewsListQuery
from domain.news.entities import NewsEntity
from domain.news.value_objects.news import TitleValueObject


@pytest.mark.asyncio
async def test_get_news_list_query_success(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    for _ in range(5):
        news = valid_news_entity_with_category("События")
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    news_list, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(news_list) == 5
    assert total == 5
    assert all(isinstance(news, NewsEntity) for news in news_list)


@pytest.mark.asyncio
async def test_get_news_list_query_with_pagination(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    for _ in range(5):
        news = valid_news_entity_with_category()
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    news_list, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(news_list) == 2
    assert total == 5

    news_list, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(news_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_news_list_query_with_category_filter(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    for _ in range(3):
        news = valid_news_entity_with_category("События")
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    for _ in range(2):
        news = valid_news_entity_with_category("Полезное")
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    news_list, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="События",
        ),
    )

    assert len(news_list) == 3
    assert total == 3
    assert all(news.category.as_generic_type() == "События" for news in news_list)


@pytest.mark.asyncio
async def test_get_news_list_query_with_search(
    mediator: Mediator,
    valid_news_entity_with_category,
    faker: Faker,
):
    news1 = valid_news_entity_with_category()
    news1 = NewsEntity(
        category=news1.category,
        title=TitleValueObject(value="Python programming"),
        slug=news1.slug,
        content=news1.content,
        short_content=news1.short_content,
        image_url=news1.image_url,
        alt=news1.alt,
        reading_time=news1.reading_time,
        date=news1.date,
    )
    await mediator.handle_command(
        CreateNewsCommand(news=news1),
    )

    news2 = valid_news_entity_with_category()
    news2 = NewsEntity(
        category=news2.category,
        title=TitleValueObject(value="JavaScript development"),
        slug=news2.slug,
        content=news2.content,
        short_content=news2.short_content,
        image_url=news2.image_url,
        alt=news2.alt,
        reading_time=news2.reading_time,
        date=news2.date,
    )
    await mediator.handle_command(
        CreateNewsCommand(news=news2),
    )

    news_list, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(news_list) == 1
    assert total == 1
    assert "Python" in news_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_news_list_query_with_sorting(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    news1 = valid_news_entity_with_category()
    news1 = NewsEntity(
        category=news1.category,
        title=TitleValueObject(value="First News"),
        slug=news1.slug,
        content=news1.content,
        short_content=news1.short_content,
        image_url=news1.image_url,
        alt=news1.alt,
        reading_time=news1.reading_time,
        date=news1.date,
    )
    await mediator.handle_command(
        CreateNewsCommand(news=news1),
    )

    news2 = valid_news_entity_with_category()
    news2 = NewsEntity(
        category=news2.category,
        title=TitleValueObject(value="Second News"),
        slug=news2.slug,
        content=news2.content,
        short_content=news2.short_content,
        image_url=news2.image_url,
        alt=news2.alt,
        reading_time=news2.reading_time,
        date=news2.date,
    )
    await mediator.handle_command(
        CreateNewsCommand(news=news2),
    )

    news_list, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="title",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(news_list) == 2
    assert total == 2
    assert news_list[0].title.as_generic_type() < news_list[1].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_news_list_query_count_only(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    for _ in range(3):
        news = valid_news_entity_with_category()
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    _, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_news_list_query_count_with_category(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    for _ in range(3):
        news = valid_news_entity_with_category("События")
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    for _ in range(2):
        news = valid_news_entity_with_category("Полезное")
        await mediator.handle_command(
            CreateNewsCommand(news=news),
        )

    _, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            category="События",
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_news_list_query_count_with_search(
    mediator: Mediator,
    valid_news_entity_with_category,
):
    news1 = valid_news_entity_with_category()
    news1 = NewsEntity(
        category=news1.category,
        title=TitleValueObject(value="Python tutorial"),
        slug=news1.slug,
        content=news1.content,
        short_content=news1.short_content,
        image_url=news1.image_url,
        alt=news1.alt,
        reading_time=news1.reading_time,
        date=news1.date,
    )
    await mediator.handle_command(
        CreateNewsCommand(news=news1),
    )

    news2 = valid_news_entity_with_category()
    news2 = NewsEntity(
        category=news2.category,
        title=TitleValueObject(value="JavaScript guide"),
        slug=news2.slug,
        content=news2.content,
        short_content=news2.short_content,
        image_url=news2.image_url,
        alt=news2.alt,
        reading_time=news2.reading_time,
        date=news2.date,
    )
    await mediator.handle_command(
        CreateNewsCommand(news=news2),
    )

    _, total = await mediator.handle_query(
        GetNewsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert total == 1
