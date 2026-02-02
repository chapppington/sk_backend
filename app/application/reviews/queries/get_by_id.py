from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.reviews.entities import ReviewEntity
from domain.reviews.services import ReviewService


@dataclass(frozen=True)
class GetReviewByIdQuery(BaseQuery):
    review_id: UUID


@dataclass(frozen=True)
class GetReviewByIdQueryHandler(
    BaseQueryHandler[GetReviewByIdQuery, ReviewEntity],
):
    review_service: ReviewService

    async def handle(self, query: GetReviewByIdQuery) -> ReviewEntity:
        return await self.review_service.get_by_id(query.review_id)
