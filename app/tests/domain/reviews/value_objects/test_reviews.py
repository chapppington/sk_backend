import pytest

from domain.reviews.exceptions.reviews import (
    ReviewCategoryInvalidException,
    ReviewNameEmptyException,
)
from domain.reviews.value_objects.reviews import (
    ReviewCategoryValueObject,
    ReviewContentUrlValueObject,
    ReviewImageValueObject,
    ReviewNameValueObject,
    ReviewPositionValueObject,
    ReviewShortTextValueObject,
    ReviewTextValueObject,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Сотрудники", "Сотрудники"),
        ("Клиенты", "Клиенты"),
    ],
)
def test_review_category_valid(value, expected):
    category = ReviewCategoryValueObject(value)
    assert category.as_generic_type() == expected


def test_review_category_invalid():
    with pytest.raises(ReviewCategoryInvalidException) as exc_info:
        ReviewCategoryValueObject("Другое")
    assert exc_info.value.category == "Другое"


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Иван Иванов", "Иван Иванов"),
        ("Петр Петров", "Петр Петров"),
    ],
)
def test_review_name_valid(value, expected):
    name = ReviewNameValueObject(value)
    assert name.as_generic_type() == expected


def test_review_name_invalid_empty():
    with pytest.raises(ReviewNameEmptyException):
        ReviewNameValueObject("")


def test_review_name_invalid_whitespace():
    with pytest.raises(ReviewNameEmptyException):
        ReviewNameValueObject("   ")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Инженер", "Инженер"),
        (None, None),
    ],
)
def test_review_position_valid(value, expected):
    position = ReviewPositionValueObject(value)
    assert position.as_generic_type() == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("review-1.jpg", "review-1.jpg"),
        (None, None),
    ],
)
def test_review_image_valid(value, expected):
    image = ReviewImageValueObject(value)
    assert image.as_generic_type() == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Полный отзыв...", "Полный отзыв..."),
        (None, None),
    ],
)
def test_review_text_valid(value, expected):
    text = ReviewTextValueObject(value)
    assert text.as_generic_type() == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Короткий отзыв", "Короткий отзыв"),
        (None, None),
    ],
)
def test_review_short_text_valid(value, expected):
    short_text = ReviewShortTextValueObject(value)
    assert short_text.as_generic_type() == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("https://example.com/video", "https://example.com/video"),
        (None, None),
    ],
)
def test_review_content_url_valid(value, expected):
    content_url = ReviewContentUrlValueObject(value)
    assert content_url.as_generic_type() == expected
