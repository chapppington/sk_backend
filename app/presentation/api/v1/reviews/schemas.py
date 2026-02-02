from typing import Optional
from uuid import UUID

from pydantic import BaseModel

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


class ReviewResponseSchema(BaseModel):
    oid: UUID
    name: str
    category: str
    position: Optional[str] = None
    image: Optional[str] = None
    text: Optional[str] = None
    short_text: Optional[str] = None
    content_url: Optional[str] = None
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: ReviewEntity) -> "ReviewResponseSchema":
        return cls(
            oid=entity.oid,
            name=entity.name.as_generic_type(),
            category=entity.category.as_generic_type(),
            position=entity.position.as_generic_type() if entity.position else None,
            image=entity.image.as_generic_type() if entity.image else None,
            text=entity.text.as_generic_type() if entity.text else None,
            short_text=entity.short_text.as_generic_type() if entity.short_text else None,
            content_url=entity.content_url.as_generic_type() if entity.content_url else None,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


class ReviewRequestSchema(BaseModel):
    name: str
    category: str
    position: Optional[str] = None
    image: Optional[str] = None
    text: Optional[str] = None
    short_text: Optional[str] = None
    content_url: Optional[str] = None

    def to_entity(self) -> ReviewEntity:
        position_vo = ReviewPositionValueObject(value=self.position) if self.position is not None else None
        image_vo = ReviewImageValueObject(value=self.image) if self.image is not None else None
        text_vo = ReviewTextValueObject(value=self.text) if self.text is not None else None
        short_text_vo = ReviewShortTextValueObject(value=self.short_text) if self.short_text is not None else None
        content_url_vo = ReviewContentUrlValueObject(value=self.content_url) if self.content_url is not None else None
        return ReviewEntity(
            name=ReviewNameValueObject(value=self.name),
            category=ReviewCategoryValueObject(value=self.category),
            position=position_vo,
            image=image_vo,
            text=text_vo,
            short_text=short_text_vo,
            content_url=content_url_vo,
        )
