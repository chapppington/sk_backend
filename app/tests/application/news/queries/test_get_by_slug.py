import pytest
from faker import Faker

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import GetNewsBySlugQuery
from domain.news.exceptions.news import NewsNotFoundBySlugException


@pytest.mark.asyncio
async def test_get_news_by_slug_success(
    mediator: Mediator,
    valid_news_data: dict,
):
    slug = valid_news_data["slug"]

    await mediator.handle_command(
        CreateNewsCommand(**valid_news_data),
    )

    retrieved_news = await mediator.handle_query(
        GetNewsBySlugQuery(slug=slug),
    )

    assert retrieved_news.slug.as_generic_type() == slug
    assert retrieved_news.title.as_generic_type() == valid_news_data["title"]


@pytest.mark.asyncio
async def test_get_news_by_slug_not_found(
    mediator: Mediator,
    faker: Faker,
):
    non_existent_slug = faker.slug()

    with pytest.raises(NewsNotFoundBySlugException) as exc_info:
        await mediator.handle_query(
            GetNewsBySlugQuery(slug=non_existent_slug),
        )

    assert exc_info.value.slug == non_existent_slug
