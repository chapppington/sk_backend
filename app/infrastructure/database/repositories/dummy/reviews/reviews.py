from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.reviews.entities import ReviewEntity
from domain.reviews.interfaces.repository import BaseReviewRepository


@dataclass
class DummyInMemoryReviewRepository(BaseReviewRepository):
    _saved_reviews: list[ReviewEntity] = field(default_factory=list, kw_only=True)

    async def add(self, review: ReviewEntity) -> ReviewEntity:
        self._saved_reviews.append(review)
        return review

    async def get_by_id(self, review_id: UUID) -> ReviewEntity | None:
        try:
            return next(review for review in self._saved_reviews if review.oid == review_id)
        except StopIteration:
            return None

    async def update(self, review: ReviewEntity) -> None:
        for i, saved_review in enumerate(self._saved_reviews):
            if saved_review.oid == review.oid:
                self._saved_reviews[i] = review
                return
        raise ValueError(f"Review with id {review.oid} not found")

    async def delete(self, review_id: UUID) -> None:
        self._saved_reviews = [review for review in self._saved_reviews if review.oid != review_id]

    async def find_many(
        self,
        category: str | None,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
    ) -> AsyncIterable[ReviewEntity]:
        filtered_reviews = self._saved_reviews.copy()
        if category is not None:
            filtered_reviews = [review for review in filtered_reviews if review.category.as_generic_type() == category]
        reverse = sort_order == -1
        if sort_field == "name":
            filtered_reviews.sort(key=lambda x: x.name.as_generic_type(), reverse=reverse)
        elif sort_field == "category":
            filtered_reviews.sort(key=lambda x: x.category.as_generic_type(), reverse=reverse)
        elif sort_field == "created_at":
            filtered_reviews.sort(key=lambda x: x.created_at, reverse=reverse)
        else:
            filtered_reviews.sort(key=lambda x: x.created_at, reverse=reverse)
        paginated = filtered_reviews[offset : offset + limit]
        for review in paginated:
            yield review

    async def count_many(self, category: str | None) -> int:
        if category is None:
            return len(self._saved_reviews)
        return sum(1 for review in self._saved_reviews if review.category.as_generic_type() == category)
