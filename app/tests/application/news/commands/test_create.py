import pytest
from faker import Faker

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import GetNewsByIdQuery
from domain.news.entities import NewsEntity
from domain.news.exceptions.news import NewsAlreadyExistsException
from domain.news.value_objects.news import TitleValueObject


@pytest.mark.asyncio
async def test_create_news_command_success(
    mediator: Mediator,
    valid_news_entity: NewsEntity,
):
    command = CreateNewsCommand(news=valid_news_entity)
    result, *_ = await mediator.handle_command(command)

    news: NewsEntity = result

    assert news is not None
    assert news.category.as_generic_type() == valid_news_entity.category.as_generic_type()
    assert news.title.as_generic_type() == valid_news_entity.title.as_generic_type()
    assert news.slug.as_generic_type() == valid_news_entity.slug.as_generic_type()
    assert news.content.as_generic_type() == valid_news_entity.content.as_generic_type()
    assert news.short_content.as_generic_type() == valid_news_entity.short_content.as_generic_type()
    assert news.image_url.as_generic_type() == valid_news_entity.image_url.as_generic_type()
    assert news.alt.as_generic_type() == valid_news_entity.alt.as_generic_type()
    assert news.reading_time.as_generic_type() == valid_news_entity.reading_time.as_generic_type()
    assert news.oid is not None

    retrieved_news = await mediator.handle_query(
        GetNewsByIdQuery(news_id=news.oid),
    )

    assert retrieved_news.oid == news.oid
    assert retrieved_news.slug.as_generic_type() == valid_news_entity.slug.as_generic_type()


@pytest.mark.asyncio
async def test_create_news_command_duplicate_slug(
    mediator: Mediator,
    valid_news_entity: NewsEntity,
    faker: Faker,
):
    command = CreateNewsCommand(news=valid_news_entity)
    await mediator.handle_command(command)

    duplicate_news = NewsEntity(
        category=valid_news_entity.category,
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        slug=valid_news_entity.slug,
        content=valid_news_entity.content,
        short_content=valid_news_entity.short_content,
        image_url=valid_news_entity.image_url,
        alt=valid_news_entity.alt,
        reading_time=valid_news_entity.reading_time,
        date=valid_news_entity.date,
    )

    with pytest.raises(NewsAlreadyExistsException) as exc_info:
        await mediator.handle_command(CreateNewsCommand(news=duplicate_news))

    assert exc_info.value.slug == valid_news_entity.slug.as_generic_type()
