from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.news.commands import (
    CreateNewsCommand,
    DeleteNewsCommand,
)
from application.news.queries import GetNewsByIdQuery
from domain.news.entities import NewsEntity
from domain.news.exceptions.news import NewsNotFoundException


@pytest.mark.asyncio
async def test_delete_news_command_success(
    mediator: Mediator,
    valid_news_entity: NewsEntity,
):
    create_result, *_ = await mediator.handle_command(
        CreateNewsCommand(news=valid_news_entity),
    )
    created_news: NewsEntity = create_result

    await mediator.handle_command(
        DeleteNewsCommand(news_id=created_news.oid),
    )

    with pytest.raises(NewsNotFoundException):
        await mediator.handle_query(
            GetNewsByIdQuery(news_id=created_news.oid),
        )


@pytest.mark.asyncio
async def test_delete_news_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(NewsNotFoundException) as exc_info:
        await mediator.handle_command(
            DeleteNewsCommand(news_id=non_existent_id),
        )

    assert exc_info.value.news_id == non_existent_id
