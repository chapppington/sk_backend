import pytest

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import CountManyPortfoliosQuery


@pytest.mark.asyncio
async def test_count_many_portfolios_query_success(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(3):
        data = valid_portfolio_data_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    count = await mediator.handle_query(
        CountManyPortfoliosQuery(),
    )

    assert count == 3


@pytest.mark.asyncio
async def test_count_many_portfolios_query_with_year(
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

    count = await mediator.handle_query(
        CountManyPortfoliosQuery(year=2020),
    )

    assert count == 3


@pytest.mark.asyncio
async def test_count_many_portfolios_query_with_search(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    data1 = valid_portfolio_data_with_year()
    data1["name"] = "Python tutorial"
    await mediator.handle_command(
        CreatePortfolioCommand(**data1),
    )

    data2 = valid_portfolio_data_with_year()
    data2["name"] = "JavaScript guide"
    await mediator.handle_command(
        CreatePortfolioCommand(**data2),
    )

    count = await mediator.handle_query(
        CountManyPortfoliosQuery(search="Python"),
    )

    assert count == 1
