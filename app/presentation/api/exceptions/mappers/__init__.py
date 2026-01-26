from fastapi import status

from presentation.api.exceptions.mappers.news import map_news_exception_to_status_code
from presentation.api.exceptions.mappers.portfolios import map_portfolio_exception_to_status_code
from presentation.api.exceptions.mappers.users import map_user_exception_to_status_code
from presentation.api.exceptions.mappers.vacancies import map_vacancy_exception_to_status_code

from domain.base.exceptions import DomainException
from domain.news.exceptions.news import NewsException
from domain.portfolios.exceptions.portfolios import PortfolioException
from domain.users.exceptions import UserException
from domain.vacancies.exceptions.vacancies import VacancyException


def map_domain_exception_to_status_code(exc: DomainException) -> int:
    if isinstance(exc, UserException):
        return map_user_exception_to_status_code(exc)
    if isinstance(exc, NewsException):
        return map_news_exception_to_status_code(exc)
    if isinstance(exc, VacancyException):
        return map_vacancy_exception_to_status_code(exc)
    if isinstance(exc, PortfolioException):
        return map_portfolio_exception_to_status_code(exc)
    return status.HTTP_400_BAD_REQUEST
