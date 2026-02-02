import pytest

from domain.reviews.entities import ReviewEntity
from domain.reviews.value_objects.reviews import (
    ReviewCategoryValueObject,
    ReviewContentUrlValueObject,
    ReviewImageValueObject,
    ReviewNameValueObject,
    ReviewPositionValueObject,
    ReviewShortTextValueObject,
    ReviewTextValueObject,
)


@pytest.fixture
def valid_review_entity_employee() -> ReviewEntity:
    return ReviewEntity(
        name=ReviewNameValueObject("Иван Иванов"),
        category=ReviewCategoryValueObject("Сотрудники"),
        position=ReviewPositionValueObject("Инженер"),
        image=ReviewImageValueObject("review-1.jpg"),
        text=ReviewTextValueObject("Полный отзыв..."),
        short_text=ReviewShortTextValueObject("Короткий отзыв"),
    )


@pytest.fixture
def valid_review_entity_client() -> ReviewEntity:
    return ReviewEntity(
        name=ReviewNameValueObject("ООО Рога и копыта"),
        category=ReviewCategoryValueObject("Клиенты"),
        content_url=ReviewContentUrlValueObject("https://example.com/review"),
    )


@pytest.fixture
def valid_review_entity_minimal() -> ReviewEntity:
    return ReviewEntity(
        name=ReviewNameValueObject("Минимальный отзыв"),
        category=ReviewCategoryValueObject("Сотрудники"),
    )
