from dataclasses import dataclass
from uuid import UUID

from domain.reviews.entities import ReviewEntity
from domain.reviews.exceptions import ReviewNotFoundException
from domain.reviews.interfaces.repository import BaseReviewRepository


@dataclass
class ReviewService:
    review_repository: BaseReviewRepository

    async def create(self, review: ReviewEntity) -> ReviewEntity:
        await self.review_repository.add(review)
        return review

    async def get_by_id(self, review_id: UUID) -> ReviewEntity:
        review = await self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException(review_id=review_id)
        return review

    async def update(self, review: ReviewEntity) -> ReviewEntity:
        await self.get_by_id(review.oid)
        await self.review_repository.update(review)
        return review

    async def delete(self, review_id: UUID) -> None:
        await self.get_by_id(review_id)
        await self.review_repository.delete(review_id)

    async def find_many(
        self,
        category: str | None,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> list[ReviewEntity]:
        reviews_iterable = self.review_repository.find_many(
            category=category,
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
        )
        return [review async for review in reviews_iterable]

    async def count_many(self, category: str | None) -> int:
        return await self.review_repository.count_many(category=category)
