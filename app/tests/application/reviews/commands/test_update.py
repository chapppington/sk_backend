from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.reviews.commands import (
    CreateReviewCommand,
    UpdateReviewCommand,
)
from application.reviews.queries import GetReviewByIdQuery
from domain.reviews.entities import ReviewEntity
from domain.reviews.exceptions import ReviewNotFoundException
from domain.reviews.value_objects.reviews import (
    ReviewCategoryValueObject,
    ReviewContentUrlValueObject,
    ReviewNameValueObject,
    ReviewPositionValueObject,
)


@pytest.mark.asyncio
async def test_update_review_command_success(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
):
    create_result, *_ = await mediator.handle_command(CreateReviewCommand(review=valid_review_entity_employee))
    created: ReviewEntity = create_result

    updated_entity = ReviewEntity(
        name=ReviewNameValueObject("Обновленное Имя"),
        category=ReviewCategoryValueObject("Сотрудники"),
        position=ReviewPositionValueObject("Директор"),
        image=created.image,
        text=created.text,
        short_text=created.short_text,
    )

    update_command = UpdateReviewCommand(review_id=created.oid, review=updated_entity)
    update_result, *_ = await mediator.handle_command(update_command)

    result: ReviewEntity = update_result

    assert result.oid == created.oid
    assert result.name.as_generic_type() == "Обновленное Имя"
    assert result.position is not None and result.position.as_generic_type() == "Директор"

    retrieved = await mediator.handle_query(GetReviewByIdQuery(review_id=created.oid))
    assert retrieved.name.as_generic_type() == "Обновленное Имя"


@pytest.mark.asyncio
async def test_update_review_command_client_success(
    mediator: Mediator,
    valid_review_entity_client: ReviewEntity,
):
    create_result, *_ = await mediator.handle_command(CreateReviewCommand(review=valid_review_entity_client))
    created: ReviewEntity = create_result

    updated_entity = ReviewEntity(
        name=ReviewNameValueObject("Новое название клиента"),
        category=ReviewCategoryValueObject("Клиенты"),
        content_url=ReviewContentUrlValueObject("https://example.com/updated"),
    )

    update_command = UpdateReviewCommand(review_id=created.oid, review=updated_entity)
    update_result, *_ = await mediator.handle_command(update_command)

    result: ReviewEntity = update_result

    assert result.name.as_generic_type() == "Новое название клиента"
    assert result.content_url is not None and result.content_url.as_generic_type() == "https://example.com/updated"


@pytest.mark.asyncio
async def test_update_review_command_not_found(
    mediator: Mediator,
    valid_review_entity_employee: ReviewEntity,
):
    non_existent_id = uuid4()
    command = UpdateReviewCommand(review_id=non_existent_id, review=valid_review_entity_employee)

    with pytest.raises(ReviewNotFoundException) as exc_info:
        await mediator.handle_command(command)

    assert exc_info.value.review_id == non_existent_id
