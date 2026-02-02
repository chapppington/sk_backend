import asyncio
from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.reviews.entities import ReviewEntity
from domain.reviews.services import ReviewService


@dataclass(frozen=True)
class GetReviewsListQuery(BaseQuery):
    category: str | None
    sort_field: str
    sort_order: int
    offset: int
    limit: int


@dataclass(frozen=True)
class GetReviewsListQueryHandler(
    BaseQueryHandler[GetReviewsListQuery, tuple[list[ReviewEntity], int]],
):
    review_service: ReviewService

    async def handle(
        self,
        query: GetReviewsListQuery,
    ) -> tuple[list[ReviewEntity], int]:
        reviews_task = asyncio.create_task(
            self.review_service.find_many(
                category=query.category,
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
            ),
        )
        count_task = asyncio.create_task(self.review_service.count_many(query.category))
        return await reviews_task, await count_task
