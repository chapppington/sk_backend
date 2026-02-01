from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.portfolios.value_objects import (
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


@dataclass(eq=False)
class PortfolioEntity(BaseEntity):
    name: NameValueObject
    slug: SlugValueObject
    poster: PosterUrlValueObject
    poster_alt: ImageAltValueObject
    year: YearValueObject
    description: DescriptionValueObject
    task_title: TaskTitleValueObject
    task_description: TaskDescriptionValueObject
    solution_title: SolutionTitleValueObject
    solution_description: SolutionDescriptionValueObject
    solution_subtitle: SolutionSubtitleValueObject
    solution_subdescription: SolutionSubdescriptionValueObject
    solution_image_left: SolutionImageUrlValueObject
    solution_image_left_alt: ImageAltValueObject
    solution_image_right: SolutionImageUrlValueObject
    solution_image_right_alt: ImageAltValueObject
    has_review: bool
    review_title: ReviewTitleValueObject | None = None
    review_text: ReviewTextValueObject | None = None
    review_name: ReviewNameValueObject | None = None
    review_image: ReviewImageUrlValueObject | None = None
    review_role: ReviewRoleValueObject | None = None
