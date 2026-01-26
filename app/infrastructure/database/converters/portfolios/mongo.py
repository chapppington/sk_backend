from datetime import datetime
from uuid import UUID

from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.value_objects.portfolios import (
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


def portfolio_entity_to_document(entity: PortfolioEntity) -> dict:
    document = {
        "oid": str(entity.oid),
        "name": entity.name.as_generic_type(),
        "slug": entity.slug.as_generic_type(),
        "poster": entity.poster.as_generic_type(),
        "year": entity.year.as_generic_type(),
        "task_title": entity.task_title.as_generic_type(),
        "task_description": entity.task_description.as_generic_type(),
        "solution_title": entity.solution_title.as_generic_type(),
        "solution_description": entity.solution_description.as_generic_type(),
        "solution_subtitle": entity.solution_subtitle.as_generic_type(),
        "solution_subdescription": entity.solution_subdescription.as_generic_type(),
        "solution_image_left": entity.solution_image_left.as_generic_type(),
        "solution_image_right": entity.solution_image_right.as_generic_type(),
        "description": entity.description.as_generic_type(),
        "has_review": entity.has_review,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }

    if entity.preview_video_path:
        document["preview_video_path"] = entity.preview_video_path.as_generic_type()
    if entity.full_video_path:
        document["full_video_path"] = entity.full_video_path.as_generic_type()
    if entity.review_title:
        document["review_title"] = entity.review_title.as_generic_type()
    if entity.review_text:
        document["review_text"] = entity.review_text.as_generic_type()
    if entity.review_name:
        document["review_name"] = entity.review_name.as_generic_type()
    if entity.review_image:
        document["review_image"] = entity.review_image.as_generic_type()
    if entity.review_role:
        document["review_role"] = entity.review_role.as_generic_type()

    return document


def portfolio_document_to_entity(document: dict) -> PortfolioEntity:
    return PortfolioEntity(
        oid=UUID(document["oid"]),
        name=NameValueObject(value=document["name"]),
        slug=SlugValueObject(value=document["slug"]),
        poster=PosterUrlValueObject(value=document["poster"]),
        year=YearValueObject(value=document["year"]),
        task_title=TaskTitleValueObject(value=document["task_title"]),
        task_description=TaskDescriptionValueObject(value=document["task_description"]),
        solution_title=SolutionTitleValueObject(value=document["solution_title"]),
        solution_description=SolutionDescriptionValueObject(value=document["solution_description"]),
        solution_subtitle=SolutionSubtitleValueObject(value=document["solution_subtitle"]),
        solution_subdescription=SolutionSubdescriptionValueObject(value=document["solution_subdescription"]),
        solution_image_left=SolutionImageUrlValueObject(value=document["solution_image_left"]),
        solution_image_right=SolutionImageUrlValueObject(value=document["solution_image_right"]),
        preview_video_path=VideoUrlValueObject(value=document.get("preview_video_path")),
        full_video_path=VideoUrlValueObject(value=document.get("full_video_path")),
        description=DescriptionValueObject(value=document["description"]),
        has_review=document["has_review"],
        review_title=ReviewTitleValueObject(value=document.get("review_title")),
        review_text=ReviewTextValueObject(value=document.get("review_text")),
        review_name=ReviewNameValueObject(value=document.get("review_name")),
        review_image=ReviewImageUrlValueObject(value=document.get("review_image")),
        review_role=ReviewRoleValueObject(value=document.get("review_role")),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
