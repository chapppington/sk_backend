import pytest
from faker import Faker

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import GetPortfolioBySlugQuery
from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.exceptions.portfolios import PortfolioNotFoundBySlugException


@pytest.mark.asyncio
async def test_get_portfolio_by_slug_success(
    mediator: Mediator,
    valid_portfolio_entity: PortfolioEntity,
):
    slug = valid_portfolio_entity.slug.as_generic_type()

    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=valid_portfolio_entity),
    )

    retrieved_portfolio = await mediator.handle_query(
        GetPortfolioBySlugQuery(slug=slug),
    )

    assert retrieved_portfolio.slug.as_generic_type() == slug
    assert retrieved_portfolio.name.as_generic_type() == valid_portfolio_entity.name.as_generic_type()


@pytest.mark.asyncio
async def test_get_portfolio_by_slug_not_found(
    mediator: Mediator,
    faker: Faker,
):
    non_existent_slug = faker.slug()

    with pytest.raises(PortfolioNotFoundBySlugException) as exc_info:
        await mediator.handle_query(
            GetPortfolioBySlugQuery(slug=non_existent_slug),
        )

    assert exc_info.value.slug == non_existent_slug
