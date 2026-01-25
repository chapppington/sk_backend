from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.portfolios.commands import (
    CreatePortfolioCommand,
    DeletePortfolioCommand,
)
from application.portfolios.queries import GetPortfolioByIdQuery
from domain.portfolios.exceptions.portfolios import PortfolioNotFoundException


@pytest.mark.asyncio
async def test_delete_portfolio_command_success(
    mediator: Mediator,
    valid_portfolio_data: dict,
):
    create_result, *_ = await mediator.handle_command(
        CreatePortfolioCommand(**valid_portfolio_data),
    )
    created_portfolio = create_result

    await mediator.handle_command(
        DeletePortfolioCommand(portfolio_id=created_portfolio.oid),
    )

    with pytest.raises(PortfolioNotFoundException):
        await mediator.handle_query(
            GetPortfolioByIdQuery(portfolio_id=created_portfolio.oid),
        )


@pytest.mark.asyncio
async def test_delete_portfolio_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(PortfolioNotFoundException) as exc_info:
        await mediator.handle_command(
            DeletePortfolioCommand(portfolio_id=non_existent_id),
        )

    assert exc_info.value.portfolio_id == non_existent_id
