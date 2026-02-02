from fastapi import status

from domain.reviews.exceptions.reviews import (
    ReviewException,
    ReviewNotFoundException,
)


def map_review_exception_to_status_code(exc: ReviewException) -> int:
    if isinstance(exc, ReviewNotFoundException):
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST
