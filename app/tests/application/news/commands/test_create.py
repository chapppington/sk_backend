import pytest
from faker import Faker

from application.mediator import Mediator
from application.news.commands import CreateNewsCommand
from application.news.queries import GetNewsByIdQuery
from domain.news.entities import NewsEntity
from domain.news.exceptions.news import (
    AltTooLongException,
    CategoryInvalidException,
    ContentEmptyException,
    NewsAlreadyExistsException,
    ReadingTimeInvalidException,
    ShortContentEmptyException,
    ShortContentTooLongException,
    SlugEmptyException,
    SlugInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)


@pytest.mark.asyncio
async def test_create_news_command_success(
    mediator: Mediator,
    valid_news_data: dict,
):
    result, *_ = await mediator.handle_command(
        CreateNewsCommand(**valid_news_data),
    )

    news: NewsEntity = result

    assert news is not None
    assert news.category.as_generic_type() == valid_news_data["category"]
    assert news.title.as_generic_type() == valid_news_data["title"]
    assert news.slug.as_generic_type() == valid_news_data["slug"]
    assert news.content.as_generic_type() == valid_news_data["content"]
    assert news.short_content.as_generic_type() == valid_news_data["short_content"]
    assert news.image_url.as_generic_type() == valid_news_data["image_url"]
    assert news.alt.as_generic_type() == valid_news_data["alt"]
    assert news.reading_time.as_generic_type() == valid_news_data["reading_time"]
    assert news.oid is not None

    retrieved_news = await mediator.handle_query(
        GetNewsByIdQuery(news_id=news.oid),
    )

    assert retrieved_news.oid == news.oid
    assert retrieved_news.slug.as_generic_type() == valid_news_data["slug"]


@pytest.mark.asyncio
async def test_create_news_command_invalid_category(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["category"] = "InvalidCategory"

    with pytest.raises(CategoryInvalidException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.category == "InvalidCategory"


@pytest.mark.asyncio
async def test_create_news_command_empty_title(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["title"] = ""

    with pytest.raises(TitleEmptyException):
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )


@pytest.mark.asyncio
async def test_create_news_command_title_too_long(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["title"] = "a" * 256

    with pytest.raises(TitleTooLongException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.title_length == 256
    assert exc_info.value.max_length == 255


@pytest.mark.asyncio
async def test_create_news_command_empty_slug(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["slug"] = ""

    with pytest.raises(SlugEmptyException):
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )


@pytest.mark.asyncio
async def test_create_news_command_invalid_slug(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["slug"] = "invalid slug with spaces"

    with pytest.raises(SlugInvalidException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.slug == "invalid slug with spaces"


@pytest.mark.asyncio
async def test_create_news_command_empty_content(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["content"] = ""

    with pytest.raises(ContentEmptyException):
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )


@pytest.mark.asyncio
async def test_create_news_command_empty_short_content(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["short_content"] = ""

    with pytest.raises(ShortContentEmptyException):
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )


@pytest.mark.asyncio
async def test_create_news_command_short_content_too_long(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["short_content"] = "a" * 501

    with pytest.raises(ShortContentTooLongException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.content_length == 501
    assert exc_info.value.max_length == 500


@pytest.mark.asyncio
async def test_create_news_command_invalid_reading_time(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["reading_time"] = 0

    with pytest.raises(ReadingTimeInvalidException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.reading_time == 0


@pytest.mark.asyncio
async def test_create_news_command_alt_too_long(
    mediator: Mediator,
    valid_news_data: dict,
):
    valid_news_data["alt"] = "a" * 256

    with pytest.raises(AltTooLongException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.alt_length == 256
    assert exc_info.value.max_length == 255


@pytest.mark.asyncio
async def test_create_news_command_duplicate_slug(
    mediator: Mediator,
    valid_news_data: dict,
    faker: Faker,
):
    slug = valid_news_data["slug"]

    await mediator.handle_command(
        CreateNewsCommand(**valid_news_data),
    )

    valid_news_data["title"] = faker.sentence(nb_words=5)

    with pytest.raises(NewsAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            CreateNewsCommand(**valid_news_data),
        )

    assert exc_info.value.slug == slug
