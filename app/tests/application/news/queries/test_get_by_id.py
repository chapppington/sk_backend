from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import GetNewsByIdQuery
from domain.news.entities import NewsEntity
from domain.news.exceptions.news import NewsNotFoundException


@pytest.mark.asyncio
async def test_get_news_by_id_success(
    mediator: Mediator,
    valid_news_data: dict,
):
    create_result, *_ = await mediator.handle_command(
        CreateNewsCommand(**valid_news_data),
    )
    created_news: NewsEntity = create_result

    retrieved_news = await mediator.handle_query(
        GetNewsByIdQuery(news_id=created_news.oid),
    )

    assert retrieved_news.oid == created_news.oid
    assert retrieved_news.category.as_generic_type() == valid_news_data["category"]
    assert retrieved_news.title.as_generic_type() == valid_news_data["title"]
    assert retrieved_news.slug.as_generic_type() == valid_news_data["slug"]


@pytest.mark.asyncio
async def test_get_news_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(NewsNotFoundException) as exc_info:
        await mediator.handle_query(
            GetNewsByIdQuery(news_id=non_existent_id),
        )

    assert exc_info.value.news_id == non_existent_id
