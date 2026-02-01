from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.services.portfolios import PortfolioService


@dataclass(frozen=True)
class UpdatePortfolioCommand(BaseCommand):
    portfolio_id: UUID
    portfolio: PortfolioEntity


@dataclass(frozen=True)
class UpdatePortfolioCommandHandler(
    BaseCommandHandler[UpdatePortfolioCommand, PortfolioEntity],
):
    portfolio_service: PortfolioService

    async def handle(self, command: UpdatePortfolioCommand) -> PortfolioEntity:
        existing_portfolio = await self.portfolio_service.get_by_id(command.portfolio_id)

        updated_portfolio = PortfolioEntity(
            oid=existing_portfolio.oid,
            created_at=existing_portfolio.created_at,
            name=command.portfolio.name,
            slug=command.portfolio.slug,
            poster=command.portfolio.poster,
            poster_alt=command.portfolio.poster_alt,
            year=command.portfolio.year,
            description=command.portfolio.description,
            task_title=command.portfolio.task_title,
            task_description=command.portfolio.task_description,
            solution_title=command.portfolio.solution_title,
            solution_description=command.portfolio.solution_description,
            solution_subtitle=command.portfolio.solution_subtitle,
            solution_subdescription=command.portfolio.solution_subdescription,
            solution_image_left=command.portfolio.solution_image_left,
            solution_image_left_alt=command.portfolio.solution_image_left_alt,
            solution_image_right=command.portfolio.solution_image_right,
            solution_image_right_alt=command.portfolio.solution_image_right_alt,
            has_review=command.portfolio.has_review,
            review_title=command.portfolio.review_title,
            review_text=command.portfolio.review_text,
            review_name=command.portfolio.review_name,
            review_image=command.portfolio.review_image,
            review_role=command.portfolio.review_role,
        )

        return await self.portfolio_service.update(updated_portfolio)
