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
from domain.news.value_objects.news import (
    SlugValueObject,
    TitleValueObject,
)


@pytest.mark.asyncio
async def test_update_news_command_success(
    mediator: Mediator,
    valid_news_entity: NewsEntity,
):
    create_command = CreateNewsCommand(news=valid_news_entity)
    create_result, *_ = await mediator.handle_command(create_command)
    created_news: NewsEntity = create_result

    updated_news = NewsEntity(
        category=created_news.category,
        title=TitleValueObject(value="Updated Title"),
        slug=created_news.slug,
        content=created_news.content,
        short_content=created_news.short_content,
        image_url=created_news.image_url,
        alt=created_news.alt,
        reading_time=created_news.reading_time,
        date=created_news.date,
    )

    update_command = UpdateNewsCommand(news_id=created_news.oid, news=updated_news)
    update_result, *_ = await mediator.handle_command(update_command)

    updated: NewsEntity = update_result

    assert updated.oid == created_news.oid
    assert updated.title.as_generic_type() == "Updated Title"
    assert updated.slug.as_generic_type() == created_news.slug.as_generic_type()

    retrieved_news = await mediator.handle_query(
        GetNewsByIdQuery(news_id=created_news.oid),
    )

    assert retrieved_news.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_news_command_not_found(
    mediator: Mediator,
    valid_news_entity: NewsEntity,
):
    non_existent_id = uuid4()
    update_command = UpdateNewsCommand(news_id=non_existent_id, news=valid_news_entity)

    with pytest.raises(NewsNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.news_id == non_existent_id


@pytest.mark.asyncio
async def test_update_news_command_duplicate_slug(
    mediator: Mediator,
    valid_news_entity: NewsEntity,
    faker: Faker,
):
    news1 = NewsEntity(
        category=valid_news_entity.category,
        title=valid_news_entity.title,
        slug=valid_news_entity.slug,
        content=valid_news_entity.content,
        short_content=valid_news_entity.short_content,
        image_url=valid_news_entity.image_url,
        alt=valid_news_entity.alt,
        reading_time=valid_news_entity.reading_time,
        date=valid_news_entity.date,
    )

    news2 = NewsEntity(
        category=valid_news_entity.category,
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        slug=SlugValueObject(value=faker.slug()),
        content=valid_news_entity.content,
        short_content=valid_news_entity.short_content,
        image_url=valid_news_entity.image_url,
        alt=valid_news_entity.alt,
        reading_time=valid_news_entity.reading_time,
        date=valid_news_entity.date,
    )

    create_result1, *_ = await mediator.handle_command(CreateNewsCommand(news=news1))
    created_news1: NewsEntity = create_result1

    create_result2, *_ = await mediator.handle_command(CreateNewsCommand(news=news2))
    created_news2: NewsEntity = create_result2

    updated_news = NewsEntity(
        category=created_news1.category,
        title=created_news1.title,
        slug=created_news2.slug,
        content=created_news1.content,
        short_content=created_news1.short_content,
        image_url=created_news1.image_url,
        alt=created_news1.alt,
        reading_time=created_news1.reading_time,
        date=created_news1.date,
    )

    update_command = UpdateNewsCommand(news_id=created_news1.oid, news=updated_news)

    with pytest.raises(NewsAlreadyExistsException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.slug == created_news2.slug.as_generic_type()
