from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.value_objects.portfolios import (
    DescriptionValueObject,
    ImageAltValueObject,
    NameValueObject,
    PosterUrlValueObject,
    ReviewImageUrlValueObject,
    ReviewNameValueObject,
    ReviewRoleValueObject,
    ReviewTextValueObject,
    ReviewTitleValueObject,
    SlugValueObject,
    SolutionDescriptionValueObject,
    SolutionImageUrlValueObject,
    SolutionSubdescriptionValueObject,
    SolutionSubtitleValueObject,
    SolutionTitleValueObject,
    TaskDescriptionValueObject,
    TaskTitleValueObject,
    YearValueObject,
)


class PortfolioResponseSchema(BaseModel):
    oid: UUID
    name: str
    slug: str
    poster: str
    poster_alt: str
    year: int
    description: str
    task_title: str
    task_description: str
    solution_title: str
    solution_description: str
    solution_subtitle: str
    solution_subdescription: str
    solution_image_left: str
    solution_image_left_alt: str
    solution_image_right: str
    solution_image_right_alt: str
    has_review: bool
    review_title: Optional[str] = None
    review_text: Optional[str] = None
    review_name: Optional[str] = None
    review_image: Optional[str] = None
    review_role: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: PortfolioEntity) -> "PortfolioResponseSchema":
        return cls(
            oid=entity.oid,
            name=entity.name.as_generic_type(),
            slug=entity.slug.as_generic_type(),
            poster=entity.poster.as_generic_type(),
            poster_alt=entity.poster_alt.as_generic_type(),
            year=entity.year.as_generic_type(),
            description=entity.description.as_generic_type(),
            task_title=entity.task_title.as_generic_type(),
            task_description=entity.task_description.as_generic_type(),
            solution_title=entity.solution_title.as_generic_type(),
            solution_description=entity.solution_description.as_generic_type(),
            solution_subtitle=entity.solution_subtitle.as_generic_type(),
            solution_subdescription=entity.solution_subdescription.as_generic_type(),
            solution_image_left=entity.solution_image_left.as_generic_type(),
            solution_image_left_alt=entity.solution_image_left_alt.as_generic_type(),
            solution_image_right=entity.solution_image_right.as_generic_type(),
            solution_image_right_alt=entity.solution_image_right_alt.as_generic_type(),
            has_review=entity.has_review,
            review_title=entity.review_title.as_generic_type() if entity.review_title else None,
            review_text=entity.review_text.as_generic_type() if entity.review_text else None,
            review_name=entity.review_name.as_generic_type() if entity.review_name else None,
            review_image=entity.review_image.as_generic_type() if entity.review_image else None,
            review_role=entity.review_role.as_generic_type() if entity.review_role else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class PortfolioRequestSchema(BaseModel):
    name: str
    slug: str
    poster: str
    poster_alt: str
    year: int
    description: str
    task_title: str
    task_description: str
    solution_title: str
    solution_description: str
    solution_subtitle: str
    solution_subdescription: str
    solution_image_left: str
    solution_image_left_alt: str
    solution_image_right: str
    solution_image_right_alt: str
    has_review: bool
    review_title: Optional[str] = None
    review_text: Optional[str] = None
    review_name: Optional[str] = None
    review_image: Optional[str] = None
    review_role: Optional[str] = None

    def to_entity(self) -> PortfolioEntity:
        return PortfolioEntity(
            name=NameValueObject(value=self.name),
            slug=SlugValueObject(value=self.slug),
            poster=PosterUrlValueObject(value=self.poster),
            poster_alt=ImageAltValueObject(value=self.poster_alt),
            year=YearValueObject(value=self.year),
            description=DescriptionValueObject(value=self.description),
            task_title=TaskTitleValueObject(value=self.task_title),
            task_description=TaskDescriptionValueObject(value=self.task_description),
            solution_title=SolutionTitleValueObject(value=self.solution_title),
            solution_description=SolutionDescriptionValueObject(value=self.solution_description),
            solution_subtitle=SolutionSubtitleValueObject(value=self.solution_subtitle),
            solution_subdescription=SolutionSubdescriptionValueObject(value=self.solution_subdescription),
            solution_image_left=SolutionImageUrlValueObject(value=self.solution_image_left),
            solution_image_left_alt=ImageAltValueObject(value=self.solution_image_left_alt),
            solution_image_right=SolutionImageUrlValueObject(value=self.solution_image_right),
            solution_image_right_alt=ImageAltValueObject(value=self.solution_image_right_alt),
            has_review=self.has_review,
            review_title=ReviewTitleValueObject(value=self.review_title) if self.review_title else None,
            review_text=ReviewTextValueObject(value=self.review_text) if self.review_text else None,
            review_name=ReviewNameValueObject(value=self.review_name) if self.review_name else None,
            review_image=ReviewImageUrlValueObject(value=self.review_image) if self.review_image else None,
            review_role=ReviewRoleValueObject(value=self.review_role) if self.review_role else None,
        )
