import pytest

from application.mediator import Mediator
from application.reviews.commands import CreateReviewCommand
from application.reviews.queries import GetReviewsListQuery
from domain.reviews.entities import ReviewEntity


@pytest.mark.asyncio
async def test_get_reviews_list_query_success(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
):
    for i in range(3):
        review = ReviewEntity(
            name=valid_review_entity_employee.name,
            category=valid_review_entity_employee.category,
            position=valid_review_entity_employee.position,
            image=valid_review_entity_employee.image,
            text=valid_review_entity_employee.text,
            short_text=valid_review_entity_employee.short_text,
        )
        await mediator.handle_command(CreateReviewCommand(review=review))

    reviews_list, total = await mediator.handle_query(
        GetReviewsListQuery(
            category=None,
            sort_field="created_at",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(reviews_list) == 3
    assert total == 3
    assert all(isinstance(r, ReviewEntity) for r in reviews_list)


@pytest.mark.asyncio
async def test_get_reviews_list_query_with_category_filter(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
    valid_review_entity_client: ReviewEntity,
):
    await mediator.handle_command(CreateReviewCommand(review=valid_review_entity_employee))
    await mediator.handle_command(CreateReviewCommand(review=valid_review_entity_employee))
    await mediator.handle_command(CreateReviewCommand(review=valid_review_entity_client))

    employees_list, employees_total = await mediator.handle_query(
        GetReviewsListQuery(
            category="Сотрудники",
            sort_field="created_at",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(employees_list) == 2
    assert employees_total == 2
    assert all(r.category.as_generic_type() == "Сотрудники" for r in employees_list)

    clients_list, clients_total = await mediator.handle_query(
        GetReviewsListQuery(
            category="Клиенты",
            sort_field="created_at",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(clients_list) == 1
    assert clients_total == 1
    assert clients_list[0].category.as_generic_type() == "Клиенты"


@pytest.mark.asyncio
async def test_get_reviews_list_query_with_pagination(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
):
    for i in range(5):
        review = ReviewEntity(
            name=valid_review_entity_employee.name,
            category=valid_review_entity_employee.category,
            position=valid_review_entity_employee.position,
            image=valid_review_entity_employee.image,
            text=valid_review_entity_employee.text,
            short_text=valid_review_entity_employee.short_text,
        )
        await mediator.handle_command(CreateReviewCommand(review=review))

    reviews_list, total = await mediator.handle_query(
        GetReviewsListQuery(
            category=None,
            sort_field="created_at",
            sort_order=1,
            offset=0,
            limit=2,
        ),
    )

    assert len(reviews_list) == 2
    assert total == 5

    reviews_list, total = await mediator.handle_query(
        GetReviewsListQuery(
            category=None,
            sort_field="created_at",
            sort_order=1,
            offset=2,
            limit=2,
        ),
    )

    assert len(reviews_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_reviews_list_query_empty(mediator: Mediator):
    reviews_list, total = await mediator.handle_query(
        GetReviewsListQuery(
            category=None,
            sort_field="created_at",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(reviews_list) == 0
    assert total == 0
