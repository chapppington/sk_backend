from uuid import uuid4

import pytest
from faker import Faker

from application.mediator import Mediator
from application.portfolios.commands import (
    CreatePortfolioCommand,
    UpdatePortfolioCommand,
)
from application.portfolios.queries import GetPortfolioByIdQuery
from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.exceptions.portfolios import (
    PortfolioAlreadyExistsException,
    PortfolioNotFoundException,
)
from domain.portfolios.value_objects.portfolios import (
    NameValueObject,
    SlugValueObject,
)


@pytest.mark.asyncio
async def test_update_portfolio_command_success(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
):
    create_command = CreatePortfolioCommand(portfolio=valid_portfolio_entity)
    create_result, *_ = await mediator.handle_command(create_command)
    created_portfolio: PortfolioEntity = create_result

    updated_portfolio = PortfolioEntity(
        name=NameValueObject(value="Updated Name"),
        slug=created_portfolio.slug,
        poster=created_portfolio.poster,
        poster_alt=created_portfolio.poster_alt,
        year=created_portfolio.year,
        description=created_portfolio.description,
        task_title=created_portfolio.task_title,
        task_description=created_portfolio.task_description,
        solution_title=created_portfolio.solution_title,
        solution_description=created_portfolio.solution_description,
        solution_subtitle=created_portfolio.solution_subtitle,
        solution_subdescription=created_portfolio.solution_subdescription,
        solution_image_left=created_portfolio.solution_image_left,
        solution_image_left_alt=created_portfolio.solution_image_left_alt,
        solution_image_right=created_portfolio.solution_image_right,
        solution_image_right_alt=created_portfolio.solution_image_right_alt,
        has_review=created_portfolio.has_review,
        review_title=created_portfolio.review_title,
        review_text=created_portfolio.review_text,
        review_name=created_portfolio.review_name,
        review_image=created_portfolio.review_image,
        review_role=created_portfolio.review_role,
    )

    update_command = UpdatePortfolioCommand(portfolio_id=created_portfolio.oid, portfolio=updated_portfolio)
    update_result, *_ = await mediator.handle_command(update_command)

    updated: PortfolioEntity = update_result

    assert updated.oid == created_portfolio.oid
    assert updated.name.as_generic_type() == "Updated Name"
    assert updated.slug.as_generic_type() == created_portfolio.slug.as_generic_type()

    retrieved_portfolio = await mediator.handle_query(
        GetPortfolioByIdQuery(portfolio_id=created_portfolio.oid),
    )

    assert retrieved_portfolio.name.as_generic_type() == "Updated Name"


@pytest.mark.asyncio
async def test_update_portfolio_command_not_found(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
):
    non_existent_id = uuid4()
    update_command = UpdatePortfolioCommand(portfolio_id=non_existent_id, portfolio=valid_portfolio_entity)

    with pytest.raises(PortfolioNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.portfolio_id == non_existent_id


@pytest.mark.asyncio
async def test_update_portfolio_command_duplicate_slug(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
    faker: Faker,
):
    portfolio1 = PortfolioEntity(
        name=valid_portfolio_entity.name,
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

    portfolio2 = PortfolioEntity(
        name=NameValueObject(value=faker.sentence(nb_words=3)),
        slug=SlugValueObject(value=faker.slug()),
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

    create_result1, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=portfolio1))
    created_portfolio1: PortfolioEntity = create_result1

    create_result2, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=portfolio2))
    created_portfolio2: PortfolioEntity = create_result2

    updated_portfolio = PortfolioEntity(
        name=created_portfolio1.name,
        slug=created_portfolio2.slug,
        poster=created_portfolio1.poster,
        poster_alt=created_portfolio1.poster_alt,
        year=created_portfolio1.year,
        description=created_portfolio1.description,
        task_title=created_portfolio1.task_title,
        task_description=created_portfolio1.task_description,
        solution_title=created_portfolio1.solution_title,
        solution_description=created_portfolio1.solution_description,
        solution_subtitle=created_portfolio1.solution_subtitle,
        solution_subdescription=created_portfolio1.solution_subdescription,
        solution_image_left=created_portfolio1.solution_image_left,
        solution_image_left_alt=created_portfolio1.solution_image_left_alt,
        solution_image_right=created_portfolio1.solution_image_right,
        solution_image_right_alt=created_portfolio1.solution_image_right_alt,
        has_review=created_portfolio1.has_review,
        review_title=created_portfolio1.review_title,
        review_text=created_portfolio1.review_text,
        review_name=created_portfolio1.review_name,
        review_image=created_portfolio1.review_image,
        review_role=created_portfolio1.review_role,
    )

    update_command = UpdatePortfolioCommand(portfolio_id=created_portfolio1.oid, portfolio=updated_portfolio)

    with pytest.raises(PortfolioAlreadyExistsException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.slug == created_portfolio2.slug.as_generic_type()
