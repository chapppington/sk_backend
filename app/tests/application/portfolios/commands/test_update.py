from uuid import uuid4

import pytest
from faker import Faker

from application.mediator import Mediator
from application.portfolios.commands import (
    CreatePortfolioCommand,
    UpdatePortfolioCommand,
)
from application.portfolios.queries import GetPortfolioByIdQuery
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.exceptions.portfolios import (
    PortfolioAlreadyExistsException,
    PortfolioNotFoundException,
)


@pytest.mark.asyncio
async def test_update_portfolio_command_success(
    mediator: Mediator,
    valid_portfolio_data: dict,
    faker: Faker,
):
    create_result, *_ = await mediator.handle_command(
        CreatePortfolioCommand(**valid_portfolio_data),
    )
    created_portfolio: PortfolioEntity = create_result

    update_data = valid_portfolio_data.copy()
    update_data["portfolio_id"] = created_portfolio.oid
    update_data["name"] = "Updated Name"

    update_result, *_ = await mediator.handle_command(
        UpdatePortfolioCommand(**update_data),
    )

    updated_portfolio: PortfolioEntity = update_result

    assert updated_portfolio.oid == created_portfolio.oid
    assert updated_portfolio.name.as_generic_type() == "Updated Name"
    assert updated_portfolio.slug.as_generic_type() == update_data["slug"]

    retrieved_portfolio = await mediator.handle_query(
        GetPortfolioByIdQuery(portfolio_id=created_portfolio.oid),
    )

    assert retrieved_portfolio.name.as_generic_type() == "Updated Name"


@pytest.mark.asyncio
async def test_update_portfolio_command_not_found(mediator: Mediator, valid_portfolio_data: dict):
    update_data = valid_portfolio_data.copy()
    update_data["portfolio_id"] = uuid4()

    with pytest.raises(PortfolioNotFoundException) as exc_info:
        await mediator.handle_command(
            UpdatePortfolioCommand(**update_data),
        )

    assert exc_info.value.portfolio_id == update_data["portfolio_id"]


@pytest.mark.asyncio
async def test_update_portfolio_command_duplicate_slug(
    mediator: Mediator,
    valid_portfolio_data: dict,
    faker: Faker,
):
    data1 = valid_portfolio_data.copy()
    data2 = valid_portfolio_data.copy()
    data2["slug"] = faker.slug()

    create_result1, *_ = await mediator.handle_command(
        CreatePortfolioCommand(**data1),
    )
    created_portfolio1: PortfolioEntity = create_result1

    await mediator.handle_command(
        CreatePortfolioCommand(**data2),
    )

    update_data = valid_portfolio_data.copy()
    update_data["portfolio_id"] = created_portfolio1.oid
    update_data["slug"] = data2["slug"]

    with pytest.raises(PortfolioAlreadyExistsException) as exc_info:
        await mediator.handle_command(
            UpdatePortfolioCommand(**update_data),
        )

    assert exc_info.value.slug == data2["slug"]
