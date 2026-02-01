import pytest
from faker import Faker

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import GetPortfolioByIdQuery
from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.exceptions.portfolios import PortfolioAlreadyExistsException
from domain.portfolios.value_objects.portfolios import NameValueObject


@pytest.mark.asyncio
async def test_create_portfolio_command_success(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
):
    command = CreatePortfolioCommand(portfolio=valid_portfolio_entity)
    result, *_ = await mediator.handle_command(command)

    portfolio: PortfolioEntity = result

    assert portfolio is not None
    assert portfolio.name.as_generic_type() == valid_portfolio_entity.name.as_generic_type()
    assert portfolio.slug.as_generic_type() == valid_portfolio_entity.slug.as_generic_type()
    assert portfolio.poster.as_generic_type() == valid_portfolio_entity.poster.as_generic_type()
    assert portfolio.year.as_generic_type() == valid_portfolio_entity.year.as_generic_type()
    assert portfolio.oid is not None

    retrieved_portfolio = await mediator.handle_query(
        GetPortfolioByIdQuery(portfolio_id=portfolio.oid),
    )

    assert retrieved_portfolio.oid == portfolio.oid
    assert retrieved_portfolio.slug.as_generic_type() == valid_portfolio_entity.slug.as_generic_type()


@pytest.mark.asyncio
async def test_create_portfolio_command_with_review(
    mediator: Mediator,
    valid_portfolio_entity_with_review: PortfolioEntity,
):
    result, *_ = await mediator.handle_command(
        CreatePortfolioCommand(portfolio=valid_portfolio_entity_with_review),
    )

    portfolio: PortfolioEntity = result

    assert portfolio.has_review is True
    assert portfolio.review_title is not None
    assert portfolio.review_text is not None
    assert portfolio.review_name is not None
    assert portfolio.review_image is not None
    assert portfolio.review_role is not None


@pytest.mark.asyncio
async def test_create_portfolio_command_duplicate_slug(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
    faker: Faker,
):
    command = CreatePortfolioCommand(portfolio=valid_portfolio_entity)
    await mediator.handle_command(command)

    duplicate_portfolio = PortfolioEntity(
        name=NameValueObject(value=faker.sentence(nb_words=3)),
        slug=valid_portfolio_entity.slug,
        poster=valid_portfolio_entity.poster,
        poster_alt=valid_portfolio_entity.poster_alt,
        year=valid_portfolio_entity.year,
        description=valid_portfolio_entity.description,
        task_title=valid_portfolio_entity.task_title,
        task_description=valid_portfolio_entity.task_description,
        solution_title=valid_portfolio_entity.solution_title,
        solution_description=valid_portfolio_entity.solution_description,
        solution_subtitle=valid_portfolio_entity.solution_subtitle,
        solution_subdescription=valid_portfolio_entity.solution_subdescription,
        solution_image_left=valid_portfolio_entity.solution_image_left,
        solution_image_left_alt=valid_portfolio_entity.solution_image_left_alt,
        solution_image_right=valid_portfolio_entity.solution_image_right,
        solution_image_right_alt=valid_portfolio_entity.solution_image_right_alt,
        has_review=valid_portfolio_entity.has_review,
        review_title=valid_portfolio_entity.review_title,
        review_text=valid_portfolio_entity.review_text,
        review_name=valid_portfolio_entity.review_name,
        review_image=valid_portfolio_entity.review_image,
        review_role=valid_portfolio_entity.review_role,
    )

    with pytest.raises(PortfolioAlreadyExistsException) as exc_info:
        await mediator.handle_command(CreatePortfolioCommand(portfolio=duplicate_portfolio))

    assert exc_info.value.slug == valid_portfolio_entity.slug.as_generic_type()
