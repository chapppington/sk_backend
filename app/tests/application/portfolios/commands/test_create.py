import pytest
from faker import Faker

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import GetPortfolioByIdQuery
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.exceptions.portfolios import (
    DescriptionEmptyException,
    NameEmptyException,
    NameTooLongException,
    PortfolioAlreadyExistsException,
    PosterUrlInvalidException,
    ReviewImageUrlInvalidException,
    SlugEmptyException,
    SlugInvalidException,
    SolutionDescriptionEmptyException,
    SolutionImageUrlInvalidException,
    SolutionSubdescriptionEmptyException,
    SolutionSubtitleEmptyException,
    SolutionTitleEmptyException,
    TaskDescriptionEmptyException,
    TaskTitleEmptyException,
    VideoUrlInvalidException,
    YearInvalidException,
)


@pytest.mark.asyncio
async def test_create_portfolio_command_success(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    result, *_ = await mediator.handle_command(
        CreatePortfolioCommand(**valid_portfolio_data),
    )

    portfolio: PortfolioEntity = result

    assert portfolio is not None
    assert portfolio.name.as_generic_type() == valid_portfolio_data["name"]
    assert portfolio.slug.as_generic_type() == valid_portfolio_data["slug"]
    assert portfolio.poster.as_generic_type() == valid_portfolio_data["poster"]
    assert portfolio.year.as_generic_type() == valid_portfolio_data["year"]
    assert portfolio.oid is not None

    retrieved_portfolio = await mediator.handle_query(
        GetPortfolioByIdQuery(portfolio_id=portfolio.oid),
    )

    assert retrieved_portfolio.oid == portfolio.oid
    assert retrieved_portfolio.slug.as_generic_type() == valid_portfolio_data["slug"]


@pytest.mark.asyncio
async def test_create_portfolio_command_with_review(
    mediator: Mediator,
    valid_portfolio_data_with_review: dict,
):
    result, *_ = await mediator.handle_command(
        CreatePortfolioCommand(**valid_portfolio_data_with_review),
    )

    portfolio: PortfolioEntity = result

    assert portfolio.has_review is True
    assert portfolio.review_title is not None
    assert portfolio.review_text is not None
    assert portfolio.review_name is not None
    assert portfolio.review_image is not None
    assert portfolio.review_role is not None


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_name(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["name"] = ""

    with pytest.raises(NameEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_name_too_long(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["name"] = "a" * 256

    with pytest.raises(NameTooLongException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.name_length == 256
    assert exc_info.value.max_length == 255


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_slug(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["slug"] = ""

    with pytest.raises(SlugEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_invalid_slug(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["slug"] = "invalid slug with spaces"

    with pytest.raises(SlugInvalidException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.slug == "invalid slug with spaces"


@pytest.mark.asyncio
async def test_create_portfolio_command_invalid_poster_url(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["poster"] = "not-a-url"

    with pytest.raises(PosterUrlInvalidException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.url == "not-a-url"


@pytest.mark.asyncio
async def test_create_portfolio_command_invalid_year(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["year"] = 1999

    with pytest.raises(YearInvalidException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.year == 1999


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_task_title(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["task_title"] = ""

    with pytest.raises(TaskTitleEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_task_description(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["task_description"] = ""

    with pytest.raises(TaskDescriptionEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_solution_title(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["solution_title"] = ""

    with pytest.raises(SolutionTitleEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_solution_description(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["solution_description"] = ""

    with pytest.raises(SolutionDescriptionEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_solution_subtitle(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["solution_subtitle"] = ""

    with pytest.raises(SolutionSubtitleEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_solution_subdescription(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["solution_subdescription"] = ""

    with pytest.raises(SolutionSubdescriptionEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_invalid_solution_image_url(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["solution_image_left"] = "not-a-url"

    with pytest.raises(SolutionImageUrlInvalidException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.url == "not-a-url"


@pytest.mark.asyncio
async def test_create_portfolio_command_invalid_video_url(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["preview_video_path"] = "not-a-url"

    with pytest.raises(VideoUrlInvalidException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.url == "not-a-url"


@pytest.mark.asyncio
async def test_create_portfolio_command_empty_description(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    valid_portfolio_data["description"] = ""

    with pytest.raises(DescriptionEmptyException):
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )


@pytest.mark.asyncio
async def test_create_portfolio_command_invalid_review_image_url(
    mediator: Mediator,
    valid_portfolio_data_with_review: dict,
):
    valid_portfolio_data_with_review["review_image"] = "not-a-url"

    with pytest.raises(ReviewImageUrlInvalidException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data_with_review),
        )

    assert exc_info.value.url == "not-a-url"


@pytest.mark.asyncio
async def test_create_portfolio_command_duplicate_slug(
    mediator: Mediator,
    valid_portfolio_data: dict,
    faker: Faker,
):
    slug = valid_portfolio_data["slug"]

    await mediator.handle_command(
        CreatePortfolioCommand(**valid_portfolio_data),
    )

    valid_portfolio_data["name"] = faker.sentence(nb_words=3)

    with pytest.raises(PortfolioAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            CreatePortfolioCommand(**valid_portfolio_data),
        )

    assert exc_info.value.slug == slug
