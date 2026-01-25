from uuid import uuid4

import pytest
from faker import Faker

from application.mediator import Mediator
from application.news.commands import (
    CreateNewsCommand,
    UpdateNewsCommand,
)
from application.news.queries import GetNewsByIdQuery
from domain.news.entities import NewsEntity
from domain.news.exceptions.news import (
    NewsAlreadyExistsException,
    NewsNotFoundException,
)


@pytest.mark.asyncio
async def test_update_news_command_success(
    mediator: Mediator,
    valid_news_data: dict,
    faker: Faker,
):
    create_result, *_ = await mediator.handle_command(
        CreateNewsCommand(**valid_news_data),
    )
    created_news: NewsEntity = create_result

    update_data = valid_news_data.copy()
    update_data["news_id"] = created_news.oid
    update_data["title"] = "Updated Title"

    update_result, *_ = await mediator.handle_command(
        UpdateNewsCommand(**update_data),
    )

    updated_news: NewsEntity = update_result

    assert updated_news.oid == created_news.oid
    assert updated_news.title.as_generic_type() == "Updated Title"
    assert updated_news.slug.as_generic_type() == update_data["slug"]

    retrieved_news = await mediator.handle_query(
        GetNewsByIdQuery(news_id=created_news.oid),
    )

    assert retrieved_news.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_news_command_not_found(mediator: Mediator, valid_news_data: dict):
    update_data = valid_news_data.copy()
    update_data["news_id"] = uuid4()

    with pytest.raises(NewsNotFoundException) as exc_info:
        await mediator.handle_command(
            UpdateNewsCommand(**update_data),
        )

    assert exc_info.value.news_id == update_data["news_id"]


@pytest.mark.asyncio
async def test_update_news_command_duplicate_slug(
    mediator: Mediator,
    valid_news_data: dict,
    faker: Faker,
):
    data1 = valid_news_data.copy()
    data2 = valid_news_data.copy()
    data2["slug"] = faker.slug()

    create_result1, *_ = await mediator.handle_command(
        CreateNewsCommand(**data1),
    )
    created_news1: NewsEntity = create_result1

    await mediator.handle_command(
        CreateNewsCommand(**data2),
    )

    update_data = valid_news_data.copy()
    update_data["news_id"] = created_news1.oid
    update_data["slug"] = data2["slug"]

    with pytest.raises(NewsAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            UpdateNewsCommand(**update_data),
        )

    assert exc_info.value.slug == data2["slug"]
