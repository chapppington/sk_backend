from fastapi import status

from domain.base.exceptions import DomainException
from domain.certificates.exceptions.certificate_groups import CertificateGroupException
from domain.certificates.exceptions.certificates import CertificateException
from domain.news.exceptions.news import NewsException
from domain.portfolios.exceptions.portfolios import PortfolioException
from domain.products.exceptions.products import ProductException
from domain.seo_settings.exceptions.seo_settings import SeoSettingsException
from domain.submissions.exceptions.submissions import SubmissionException
from domain.users.exceptions import UserException
from domain.vacancies.exceptions.vacancies import VacancyException
from presentation.api.exceptions.mappers.certificates import (
    map_certificate_exception_to_status_code,
    map_certificate_group_exception_to_status_code,
)
from presentation.api.exceptions.mappers.news import map_news_exception_to_status_code
from presentation.api.exceptions.mappers.portfolios import map_portfolio_exception_to_status_code
from presentation.api.exceptions.mappers.products import map_product_exception_to_status_code
from presentation.api.exceptions.mappers.seo_settings import map_seo_settings_exception_to_status_code
from presentation.api.exceptions.mappers.submissions import map_submission_exception_to_status_code
from presentation.api.exceptions.mappers.users import map_user_exception_to_status_code
from presentation.api.exceptions.mappers.vacancies import map_vacancy_exception_to_status_code


def map_domain_exception_to_status_code(exc: DomainException) -> int:
    if isinstance(exc, UserException):
        return map_user_exception_to_status_code(exc)
    if isinstance(exc, NewsException):
        return map_news_exception_to_status_code(exc)
    if isinstance(exc, VacancyException):
        return map_vacancy_exception_to_status_code(exc)
    if isinstance(exc, PortfolioException):
        return map_portfolio_exception_to_status_code(exc)
    if isinstance(exc, ProductException):
        return map_product_exception_to_status_code(exc)
    if isinstance(exc, SeoSettingsException):
        return map_seo_settings_exception_to_status_code(exc)
    if isinstance(exc, CertificateGroupException):
        return map_certificate_group_exception_to_status_code(exc)
    if isinstance(exc, CertificateException):
        return map_certificate_exception_to_status_code(exc)
    if isinstance(exc, SubmissionException):
        return map_submission_exception_to_status_code(exc)
    return status.HTTP_400_BAD_REQUEST
