from dataclasses import dataclass
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.reviews.entities import ReviewEntity
from domain.reviews.services import ReviewService


@dataclass(frozen=True)
class UpdateReviewCommand(BaseCommand):
    review_id: UUID
    review: ReviewEntity


@dataclass(frozen=True)
class UpdateReviewCommandHandler(
    BaseCommandHandler[UpdateReviewCommand, ReviewEntity],
):
    review_service: ReviewService

    async def handle(self, command: UpdateReviewCommand) -> ReviewEntity:
        existing = await self.review_service.get_by_id(command.review_id)
        updated = ReviewEntity(
            oid=existing.oid,
            created_at=existing.created_at,
            name=command.review.name,
            category=command.review.category,
            position=command.review.position,
            image=command.review.image,
            text=command.review.text,
            short_text=command.review.short_text,
            content_url=command.review.content_url,
        )
        return await self.review_service.update(updated)
