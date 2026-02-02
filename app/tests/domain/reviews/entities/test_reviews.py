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


def test_review_entity_employee_creation():
    name = ReviewNameValueObject("Иван Иванов")
    category = ReviewCategoryValueObject("Сотрудники")
    position = ReviewPositionValueObject("Инженер")
    image = ReviewImageValueObject("review-1.jpg")
    text = ReviewTextValueObject("Полный отзыв...")
    short_text = ReviewShortTextValueObject("Короткий отзыв")

    review = ReviewEntity(
        name=name,
        category=category,
        position=position,
        image=image,
        text=text,
        short_text=short_text,
    )

    assert review.name.as_generic_type() == "Иван Иванов"
    assert review.category.as_generic_type() == "Сотрудники"
    assert review.position.as_generic_type() == "Инженер"
    assert review.image.as_generic_type() == "review-1.jpg"
    assert review.text.as_generic_type() == "Полный отзыв..."
    assert review.short_text.as_generic_type() == "Короткий отзыв"
    assert review.content_url is None
    assert review.oid is not None
    assert review.created_at is not None
    assert review.updated_at is not None


def test_review_entity_client_creation():
    name = ReviewNameValueObject("ООО Рога и копыта")
    category = ReviewCategoryValueObject("Клиенты")
    content_url = ReviewContentUrlValueObject("https://example.com/review")

    review = ReviewEntity(
        name=name,
        category=category,
        content_url=content_url,
    )

    assert review.name.as_generic_type() == "ООО Рога и копыта"
    assert review.category.as_generic_type() == "Клиенты"
    assert review.content_url.as_generic_type() == "https://example.com/review"
    assert review.position is None
    assert review.image is None
    assert review.text is None
    assert review.short_text is None
    assert review.oid is not None


def test_review_entity_minimal_creation():
    name = ReviewNameValueObject("Минимальный отзыв")
    category = ReviewCategoryValueObject("Сотрудники")

    review = ReviewEntity(name=name, category=category)

    assert review.name.as_generic_type() == "Минимальный отзыв"
    assert review.category.as_generic_type() == "Сотрудники"
    assert review.position is None
    assert review.image is None
    assert review.text is None
    assert review.short_text is None
    assert review.content_url is None
    assert review.oid is not None
