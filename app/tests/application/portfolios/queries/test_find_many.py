import pytest

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import FindManyPortfoliosQuery
from domain.portfolios.entities.portfolios import PortfolioEntity


@pytest.mark.asyncio
async def test_find_many_portfolios_query_success(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(5):
        data = valid_portfolio_data_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    result = await mediator.handle_query(
        FindManyPortfoliosQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    portfolio_list = [portfolio async for portfolio in result]

    assert len(portfolio_list) == 5
    assert all(isinstance(portfolio, PortfolioEntity) for portfolio in portfolio_list)


@pytest.mark.asyncio
async def test_find_many_portfolios_query_with_pagination(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(5):
        data = valid_portfolio_data_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    result = await mediator.handle_query(
        FindManyPortfoliosQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    portfolio_list = [portfolio async for portfolio in result]

    assert len(portfolio_list) == 2

    result = await mediator.handle_query(
        FindManyPortfoliosQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    portfolio_list = [portfolio async for portfolio in result]

    assert len(portfolio_list) == 2


@pytest.mark.asyncio
async def test_find_many_portfolios_query_with_year_filter(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(3):
        data = valid_portfolio_data_with_year(2020)
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    for _ in range(2):
        data = valid_portfolio_data_with_year(2021)
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    result = await mediator.handle_query(
        FindManyPortfoliosQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            year=2020,
        ),
    )

    portfolio_list = [portfolio async for portfolio in result]

    assert len(portfolio_list) == 3
    assert all(portfolio.year.as_generic_type() == 2020 for portfolio in portfolio_list)


@pytest.mark.asyncio
async def test_find_many_portfolios_query_with_search(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    data1 = valid_portfolio_data_with_year()
    data1["name"] = "Python Project"
    await mediator.handle_command(
        CreatePortfolioCommand(**data1),
    )

    data2 = valid_portfolio_data_with_year()
    data2["name"] = "JavaScript Project"
    await mediator.handle_command(
        CreatePortfolioCommand(**data2),
    )

    result = await mediator.handle_query(
        FindManyPortfoliosQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    portfolio_list = [portfolio async for portfolio in result]

    assert len(portfolio_list) == 1
    assert "Python" in portfolio_list[0].name.as_generic_type()


@pytest.mark.asyncio
async def test_find_many_portfolios_query_with_sorting(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    data1 = valid_portfolio_data_with_year()
    data1["name"] = "First Portfolio"
    await mediator.handle_command(
        CreatePortfolioCommand(**data1),
    )

    data2 = valid_portfolio_data_with_year()
    data2["name"] = "Second Portfolio"
    await mediator.handle_command(
        CreatePortfolioCommand(**data2),
    )

    result = await mediator.handle_query(
        FindManyPortfoliosQuery(
            sort_field="name",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    portfolio_list = [portfolio async for portfolio in result]

    assert len(portfolio_list) == 2
    assert portfolio_list[0].name.as_generic_type() < portfolio_list[1].name.as_generic_type()
