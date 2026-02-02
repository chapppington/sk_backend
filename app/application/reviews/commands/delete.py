from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.reviews.services import ReviewService


@dataclass(frozen=True)
class DeleteReviewCommand(BaseCommand):
    review_id: UUID


@dataclass(frozen=True)
class DeleteReviewCommandHandler(
    BaseCommandHandler[DeleteReviewCommand, None],
):
    review_service: ReviewService

    async def handle(self, command: DeleteReviewCommand) -> None:
        await self.review_service.delete(command.review_id)
