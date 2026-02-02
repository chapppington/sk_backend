from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.reviews.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
)
from application.reviews.queries import GetReviewByIdQuery
from domain.reviews.entities import ReviewEntity
from domain.reviews.exceptions import ReviewNotFoundException


@pytest.mark.asyncio
async def test_delete_review_command_success(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
):
    create_result, *_ = await mediator.handle_command(CreateReviewCommand(review=valid_review_entity_employee))
    created: ReviewEntity = create_result

    await mediator.handle_command(DeleteReviewCommand(review_id=created.oid))

    with pytest.raises(ReviewNotFoundException):
        await mediator.handle_query(GetReviewByIdQuery(review_id=created.oid))


@pytest.mark.asyncio
async def test_delete_review_command_not_found(mediator: Mediator):
    non_existent_id = uuid4()

    with pytest.raises(ReviewNotFoundException) as exc_info:
        await mediator.handle_command(DeleteReviewCommand(review_id=non_existent_id))

    assert exc_info.value.review_id == non_existent_id
