from fastapi import status

from domain.portfolios.exceptions.portfolios import (
    PortfolioAlreadyExistsException,
    PortfolioException,
    PortfolioNotFoundBySlugException,
    PortfolioNotFoundException,
)


def map_portfolio_exception_to_status_code(exc: PortfolioException) -> int:
    if isinstance(exc, (PortfolioNotFoundException, PortfolioNotFoundBySlugException)):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, PortfolioAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
