from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain.portfolios.entities.portfolios import PortfolioEntity


class PortfolioResponseSchema(BaseModel):
    oid: UUID
    name: str
    slug: str
    poster: str
    year: int
    task_title: str
    task_description: str
    solution_title: str
    solution_description: str
    solution_subtitle: str
    solution_subdescription: str
    solution_image_left: str
    solution_image_right: str
    preview_video_path: Optional[str] = None
    full_video_path: Optional[str] = None
    description: str
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
            year=entity.year.as_generic_type(),
            task_title=entity.task_title.as_generic_type(),
            task_description=entity.task_description.as_generic_type(),
            solution_title=entity.solution_title.as_generic_type(),
            solution_description=entity.solution_description.as_generic_type(),
            solution_subtitle=entity.solution_subtitle.as_generic_type(),
            solution_subdescription=entity.solution_subdescription.as_generic_type(),
            solution_image_left=entity.solution_image_left.as_generic_type(),
            solution_image_right=entity.solution_image_right.as_generic_type(),
            preview_video_path=entity.preview_video_path.as_generic_type() if entity.preview_video_path else None,
            full_video_path=entity.full_video_path.as_generic_type() if entity.full_video_path else None,
            description=entity.description.as_generic_type(),
            has_review=entity.has_review,
            review_title=entity.review_title.as_generic_type() if entity.review_title else None,
            review_text=entity.review_text.as_generic_type() if entity.review_text else None,
            review_name=entity.review_name.as_generic_type() if entity.review_name else None,
            review_image=entity.review_image.as_generic_type() if entity.review_image else None,
            review_role=entity.review_role.as_generic_type() if entity.review_role else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class CreatePortfolioRequestSchema(BaseModel):
    name: str
    slug: str
    poster: str
    year: int
    task_title: str
    task_description: str
    solution_title: str
    solution_description: str
    solution_subtitle: str
    solution_subdescription: str
    solution_image_left: str
    solution_image_right: str
    preview_video_path: Optional[str] = None
    full_video_path: Optional[str] = None
    description: str
    has_review: bool
    review_title: Optional[str] = None
    review_text: Optional[str] = None
    review_name: Optional[str] = None
    review_image: Optional[str] = None
    review_role: Optional[str] = None


class UpdatePortfolioRequestSchema(BaseModel):
    name: str
    slug: str
    poster: str
    year: int
    task_title: str
    task_description: str
    solution_title: str
    solution_description: str
    solution_subtitle: str
    solution_subdescription: str
    solution_image_left: str
    solution_image_right: str
    preview_video_path: Optional[str] = None
    full_video_path: Optional[str] = None
    description: str
    has_review: bool
    review_title: Optional[str] = None
    review_text: Optional[str] = None
    review_name: Optional[str] = None
    review_image: Optional[str] = None
    review_role: Optional[str] = None
