from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.portfolios.value_objects import (
    DescriptionValueObject,
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
    VideoUrlValueObject,
    YearValueObject,
)


@dataclass(eq=False)
class PortfolioEntity(BaseEntity):
    name: NameValueObject
    slug: SlugValueObject
    poster: PosterUrlValueObject
    year: YearValueObject
    task_title: TaskTitleValueObject
    task_description: TaskDescriptionValueObject
    solution_title: SolutionTitleValueObject
    solution_description: SolutionDescriptionValueObject
    solution_subtitle: SolutionSubtitleValueObject
    solution_subdescription: SolutionSubdescriptionValueObject
    solution_image_left: SolutionImageUrlValueObject
    solution_image_right: SolutionImageUrlValueObject
    preview_video_path: VideoUrlValueObject
    full_video_path: VideoUrlValueObject
    description: DescriptionValueObject
    has_review: bool
    review_title: ReviewTitleValueObject | None = None
    review_text: ReviewTextValueObject | None = None
    review_name: ReviewNameValueObject | None = None
    review_image: ReviewImageUrlValueObject | None = None
    review_role: ReviewRoleValueObject | None = None
