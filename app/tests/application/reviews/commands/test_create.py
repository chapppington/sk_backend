import pytest

from application.mediator import Mediator
from application.reviews.commands import CreateReviewCommand
from application.reviews.queries import GetReviewByIdQuery
from domain.reviews.entities import ReviewEntity


@pytest.mark.asyncio
async def test_create_review_command_employee_success(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
):
    command = CreateReviewCommand(review=valid_review_entity_employee)
    result, *_ = await mediator.handle_command(command)

    review: ReviewEntity = result

    assert review is not None
    assert review.name.as_generic_type() == valid_review_entity_employee.name.as_generic_type()
    assert review.category.as_generic_type() == "Сотрудники"
    assert review.position is not None and review.position.as_generic_type() == "Инженер"
    assert review.text is not None and review.text.as_generic_type() == "Полный отзыв..."
    assert review.short_text is not None and review.short_text.as_generic_type() == "Короткий отзыв"
    assert review.oid is not None

    retrieved = await mediator.handle_query(GetReviewByIdQuery(review_id=review.oid))
    assert retrieved.oid == review.oid
    assert retrieved.name.as_generic_type() == valid_review_entity_employee.name.as_generic_type()


@pytest.mark.asyncio
async def test_create_review_command_client_success(
    mediator: Mediator,
    valid_review_entity_client: ReviewEntity,
):
    command = CreateReviewCommand(review=valid_review_entity_client)
    result, *_ = await mediator.handle_command(command)

    review: ReviewEntity = result

    assert review is not None
    assert review.category.as_generic_type() == "Клиенты"
    assert review.content_url is not None
    assert review.content_url.as_generic_type() == "https://example.com/review"

    retrieved = await mediator.handle_query(GetReviewByIdQuery(review_id=review.oid))
    assert retrieved.oid == review.oid


@pytest.mark.asyncio
async def test_create_review_command_minimal_success(
    mediator: Mediator,
    valid_review_entity_minimal: ReviewEntity,
):
    command = CreateReviewCommand(review=valid_review_entity_minimal)
    result, *_ = await mediator.handle_command(command)

    review: ReviewEntity = result

    assert review is not None
    assert review.name.as_generic_type() == "Минимальный отзыв"
    assert review.position is None
    assert review.image is None
    assert review.text is None
    assert review.short_text is None
    assert review.content_url is None
