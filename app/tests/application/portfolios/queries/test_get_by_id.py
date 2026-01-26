from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import GetPortfolioByIdQuery
from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.exceptions.portfolios import PortfolioNotFoundException


@pytest.mark.asyncio
async def test_get_portfolio_by_id_success(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
):
    create_result, *_ = await mediator.handle_command(
        CreatePortfolioCommand(portfolio=valid_portfolio_entity),
    )
    created_portfolio: PortfolioEntity = create_result

    retrieved_portfolio = await mediator.handle_query(
        GetPortfolioByIdQuery(portfolio_id=created_portfolio.oid),
    )

    assert retrieved_portfolio.oid == created_portfolio.oid
    assert retrieved_portfolio.name.as_generic_type() == valid_portfolio_entity.name.as_generic_type()
    assert retrieved_portfolio.slug.as_generic_type() == valid_portfolio_entity.slug.as_generic_type()


@pytest.mark.asyncio
async def test_get_portfolio_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(PortfolioNotFoundException) as exc_info:
        await mediator.handle_query(
            GetPortfolioByIdQuery(portfolio_id=non_existent_id),
        )

    assert exc_info.value.portfolio_id == non_existent_id
