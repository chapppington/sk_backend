import pytest
from faker import Faker

from application.mediator import Mediator
from application.portfolios.commands import CreatePortfolioCommand
from application.portfolios.queries import GetPortfolioListQuery
from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.value_objects.portfolios import NameValueObject


@pytest.mark.asyncio
async def test_get_portfolio_list_query_success(
    mediator: Mediator,
    valid_portfolio_entity_with_year,
):
    for _ in range(5):
        portfolio = valid_portfolio_entity_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
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
    valid_portfolio_entity_with_year,
):
    for _ in range(5):
        portfolio = valid_portfolio_entity_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
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
    valid_portfolio_entity_with_year,
):
    for _ in range(3):
        portfolio = valid_portfolio_entity_with_year(2020)
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
        )

    for _ in range(2):
        portfolio = valid_portfolio_entity_with_year(2021)
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
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
    valid_portfolio_entity_with_year,
):
    portfolio1 = valid_portfolio_entity_with_year()
    portfolio1 = PortfolioEntity(
        name=NameValueObject(value="Python Project"),
        slug=portfolio1.slug,
        poster=portfolio1.poster,
        year=portfolio1.year,
        task_title=portfolio1.task_title,
        task_description=portfolio1.task_description,
        solution_title=portfolio1.solution_title,
        solution_description=portfolio1.solution_description,
        solution_subtitle=portfolio1.solution_subtitle,
        solution_subdescription=portfolio1.solution_subdescription,
        solution_image_left=portfolio1.solution_image_left,
        solution_image_right=portfolio1.solution_image_right,
        description=portfolio1.description,
        has_review=portfolio1.has_review,
        review_title=portfolio1.review_title,
        review_text=portfolio1.review_text,
        review_name=portfolio1.review_name,
        review_image=portfolio1.review_image,
        review_role=portfolio1.review_role,
    )
    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=portfolio1),
    )

    portfolio2 = valid_portfolio_entity_with_year()
    portfolio2 = PortfolioEntity(
        name=NameValueObject(value="JavaScript Project"),
        slug=portfolio2.slug,
        poster=portfolio2.poster,
        year=portfolio2.year,
        task_title=portfolio2.task_title,
        task_description=portfolio2.task_description,
        solution_title=portfolio2.solution_title,
        solution_description=portfolio2.solution_description,
        solution_subtitle=portfolio2.solution_subtitle,
        solution_subdescription=portfolio2.solution_subdescription,
        solution_image_left=portfolio2.solution_image_left,
        solution_image_right=portfolio2.solution_image_right,
        description=portfolio2.description,
        has_review=portfolio2.has_review,
        review_title=portfolio2.review_title,
        review_text=portfolio2.review_text,
        review_name=portfolio2.review_name,
        review_image=portfolio2.review_image,
        review_role=portfolio2.review_role,
    )
    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=portfolio2),
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
    valid_portfolio_entity_with_year,
):
    portfolio1 = valid_portfolio_entity_with_year()
    portfolio1 = PortfolioEntity(
        name=NameValueObject(value="First Portfolio"),
        slug=portfolio1.slug,
        poster=portfolio1.poster,
        year=portfolio1.year,
        task_title=portfolio1.task_title,
        task_description=portfolio1.task_description,
        solution_title=portfolio1.solution_title,
        solution_description=portfolio1.solution_description,
        solution_subtitle=portfolio1.solution_subtitle,
        solution_subdescription=portfolio1.solution_subdescription,
        solution_image_left=portfolio1.solution_image_left,
        solution_image_right=portfolio1.solution_image_right,
        description=portfolio1.description,
        has_review=portfolio1.has_review,
        review_title=portfolio1.review_title,
        review_text=portfolio1.review_text,
        review_name=portfolio1.review_name,
        review_image=portfolio1.review_image,
        review_role=portfolio1.review_role,
    )
    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=portfolio1),
    )

    portfolio2 = valid_portfolio_entity_with_year()
    portfolio2 = PortfolioEntity(
        name=NameValueObject(value="Second Portfolio"),
        slug=portfolio2.slug,
        poster=portfolio2.poster,
        year=portfolio2.year,
        task_title=portfolio2.task_title,
        task_description=portfolio2.task_description,
        solution_title=portfolio2.solution_title,
        solution_description=portfolio2.solution_description,
        solution_subtitle=portfolio2.solution_subtitle,
        solution_subdescription=portfolio2.solution_subdescription,
        solution_image_left=portfolio2.solution_image_left,
        solution_image_right=portfolio2.solution_image_right,
        description=portfolio2.description,
        has_review=portfolio2.has_review,
        review_title=portfolio2.review_title,
        review_text=portfolio2.review_text,
        review_name=portfolio2.review_name,
        review_image=portfolio2.review_image,
        review_role=portfolio2.review_role,
    )
    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=portfolio2),
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
    valid_portfolio_entity_with_year,
):
    for _ in range(3):
        portfolio = valid_portfolio_entity_with_year()
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
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
    valid_portfolio_entity_with_year,
):
    for _ in range(3):
        portfolio = valid_portfolio_entity_with_year(2020)
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
        )

    for _ in range(2):
        portfolio = valid_portfolio_entity_with_year(2021)
        await mediator.handle_command(
            CreatePortfolioCommand(portfolio=portfolio),
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
    valid_portfolio_entity_with_year,
    faker: Faker,
):
    portfolio1 = valid_portfolio_entity_with_year()
    portfolio1 = PortfolioEntity(
        name=NameValueObject(value="Python tutorial"),
        slug=portfolio1.slug,
        poster=portfolio1.poster,
        year=portfolio1.year,
        task_title=portfolio1.task_title,
        task_description=portfolio1.task_description,
        solution_title=portfolio1.solution_title,
        solution_description=portfolio1.solution_description,
        solution_subtitle=portfolio1.solution_subtitle,
        solution_subdescription=portfolio1.solution_subdescription,
        solution_image_left=portfolio1.solution_image_left,
        solution_image_right=portfolio1.solution_image_right,
        description=portfolio1.description,
        has_review=portfolio1.has_review,
        review_title=portfolio1.review_title,
        review_text=portfolio1.review_text,
        review_name=portfolio1.review_name,
        review_image=portfolio1.review_image,
        review_role=portfolio1.review_role,
    )
    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=portfolio1),
    )

    portfolio2 = valid_portfolio_entity_with_year()
    portfolio2 = PortfolioEntity(
        name=NameValueObject(value="JavaScript guide"),
        slug=portfolio2.slug,
        poster=portfolio2.poster,
        year=portfolio2.year,
        task_title=portfolio2.task_title,
        task_description=portfolio2.task_description,
        solution_title=portfolio2.solution_title,
        solution_description=portfolio2.solution_description,
        solution_subtitle=portfolio2.solution_subtitle,
        solution_subdescription=portfolio2.solution_subdescription,
        solution_image_left=portfolio2.solution_image_left,
        solution_image_right=portfolio2.solution_image_right,
        description=portfolio2.description,
        has_review=portfolio2.has_review,
        review_title=portfolio2.review_title,
        review_text=portfolio2.review_text,
        review_name=portfolio2.review_name,
        review_image=portfolio2.review_image,
        review_role=portfolio2.review_role,
    )
    await mediator.handle_command(
        CreatePortfolioCommand(portfolio=portfolio2),
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
