import pytest

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import GetPortfolioListQuery
from domain.portfolios.entities.portfolios import PortfolioEntity


@pytest.mark.asyncio
async def test_get_portfolio_list_query_success(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(5):
        data = valid_portfolio_data_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    portfolio_list, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(portfolio_list) == 5
    assert total == 5
    assert all(isinstance(portfolio, PortfolioEntity) for portfolio in portfolio_list)


@pytest.mark.asyncio
async def test_get_portfolio_list_query_with_pagination(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(5):
        data = valid_portfolio_data_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    portfolio_list, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(portfolio_list) == 2
    assert total == 5

    portfolio_list, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(portfolio_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_portfolio_list_query_with_year_filter(
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

    portfolio_list, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            year=2020,
        ),
    )

    assert len(portfolio_list) == 3
    assert total == 3
    assert all(portfolio.year.as_generic_type() == 2020 for portfolio in portfolio_list)


@pytest.mark.asyncio
async def test_get_portfolio_list_query_with_search(
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

    portfolio_list, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(portfolio_list) == 1
    assert total == 1
    assert "Python" in portfolio_list[0].name.as_generic_type()


@pytest.mark.asyncio
async def test_get_portfolio_list_query_with_sorting(
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

    portfolio_list, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="name",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(portfolio_list) == 2
    assert total == 2
    assert portfolio_list[0].name.as_generic_type() < portfolio_list[1].name.as_generic_type()


@pytest.mark.asyncio
async def test_get_portfolio_list_query_count_only(
    mediator: Mediator,
    valid_portfolio_data_with_year,
):
    for _ in range(3):
        data = valid_portfolio_data_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(**data),
        )

    _, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_portfolio_list_query_count_with_year(
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

    _, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            year=2020,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_portfolio_list_query_count_with_search(
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

    _, total = await mediator.handle_query(
        GetPortfolioListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert total == 1
