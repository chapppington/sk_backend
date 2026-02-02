from dataclasses import dataclass

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.reviews.entities import ReviewEntity
from domain.reviews.services import ReviewService


@dataclass(frozen=True)
class CreateReviewCommand(BaseCommand):
    review: ReviewEntity


@dataclass(frozen=True)
class CreateReviewCommandHandler(
    BaseCommandHandler[CreateReviewCommand, ReviewEntity],
):
    review_service: ReviewService

    async def handle(self, command: CreateReviewCommand) -> ReviewEntity:
        return await self.review_service.create(command.review)
