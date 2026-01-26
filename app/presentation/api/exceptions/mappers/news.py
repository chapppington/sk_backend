from fastapi import status

from domain.news.exceptions.news import (
    NewsAlreadyExistsException,
    NewsException,
    NewsNotFoundBySlugException,
    NewsNotFoundException,
)


def map_news_exception_to_status_code(exc: NewsException) -> int:
    if isinstance(exc, (NewsNotFoundException, NewsNotFoundBySlugException)):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, NewsAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
