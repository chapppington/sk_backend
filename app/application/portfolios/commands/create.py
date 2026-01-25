from dataclasses import dataclass
from typing import Optional

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService
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


@dataclass(frozen=True)
class CreatePortfolioCommand(BaseCommand):
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
    preview_video_path: str
    full_video_path: str
    description: str
    has_review: bool
    review_title: Optional[str] = None
    review_text: Optional[str] = None
    review_name: Optional[str] = None
    review_image: Optional[str] = None
    review_role: Optional[str] = None


@dataclass(frozen=True)
class CreatePortfolioCommandHandler(
    BaseCommandHandler[CreatePortfolioCommand, PortfolioEntity],
):
    portfolio_service: PortfolioService

    async def handle(self, command: CreatePortfolioCommand) -> PortfolioEntity:
        portfolio = PortfolioEntity(
            name=NameValueObject(value=command.name),
            slug=SlugValueObject(value=command.slug),
            poster=PosterUrlValueObject(value=command.poster),
            year=YearValueObject(value=command.year),
            task_title=TaskTitleValueObject(value=command.task_title),
            task_description=TaskDescriptionValueObject(value=command.task_description),
            solution_title=SolutionTitleValueObject(value=command.solution_title),
            solution_description=SolutionDescriptionValueObject(value=command.solution_description),
            solution_subtitle=SolutionSubtitleValueObject(value=command.solution_subtitle),
            solution_subdescription=SolutionSubdescriptionValueObject(value=command.solution_subdescription),
            solution_image_left=SolutionImageUrlValueObject(value=command.solution_image_left),
            solution_image_right=SolutionImageUrlValueObject(value=command.solution_image_right),
            preview_video_path=VideoUrlValueObject(value=command.preview_video_path),
            full_video_path=VideoUrlValueObject(value=command.full_video_path),
            description=DescriptionValueObject(value=command.description),
            has_review=command.has_review,
            review_title=ReviewTitleValueObject(value=command.review_title) if command.review_title else None,
            review_text=ReviewTextValueObject(value=command.review_text) if command.review_text else None,
            review_name=ReviewNameValueObject(value=command.review_name) if command.review_name else None,
            review_image=ReviewImageUrlValueObject(value=command.review_image) if command.review_image else None,
            review_role=ReviewRoleValueObject(value=command.review_role) if command.review_role else None,
        )

        return await self.portfolio_service.create(portfolio)
