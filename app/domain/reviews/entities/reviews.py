from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.reviews.value_objects.reviews import (
    ReviewCategoryValueObject,
    ReviewContentUrlValueObject,
    ReviewImageValueObject,
    ReviewNameValueObject,
    ReviewPositionValueObject,
    ReviewShortTextValueObject,
    ReviewTextValueObject,
)


@dataclass(eq=False)
class ReviewEntity(BaseEntity):
    name: ReviewNameValueObject
    category: ReviewCategoryValueObject
    position: ReviewPositionValueObject | None = None
    image: ReviewImageValueObject | None = None
    text: ReviewTextValueObject | None = None
    short_text: ReviewShortTextValueObject | None = None
    content_url: ReviewContentUrlValueObject | None = None
