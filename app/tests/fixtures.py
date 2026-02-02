from punq import (
    Container,
    Scope,
)

from application.container import _init_container
from domain.certificates.interfaces.repositories.certificate_groups import BaseCertificateGroupRepository
from domain.certificates.interfaces.repositories.certificates import BaseCertificateRepository
from domain.members.interfaces.repository import BaseMemberRepository
from domain.news.interfaces.repository import BaseNewsRepository
from domain.portfolios.interfaces.repository import BasePortfolioRepository
from domain.products.interfaces.repository import BaseProductRepository
from domain.seo_settings.interfaces.repository import BaseSeoSettingsRepository
from domain.submissions.interfaces.repository import BaseSubmissionRepository
from domain.users.interfaces.repository import BaseUserRepository
from domain.vacancies.interfaces.repository import BaseVacancyRepository
from infrastructure.database.repositories.dummy.certificates import (
    DummyInMemoryCertificateGroupRepository,
    DummyInMemoryCertificateRepository,
)
from infrastructure.database.repositories.dummy.members.members import DummyInMemoryMemberRepository
from infrastructure.database.repositories.dummy.news.news import DummyInMemoryNewsRepository
from infrastructure.database.repositories.dummy.portfolios.portfolios import DummyInMemoryPortfolioRepository
from infrastructure.database.repositories.dummy.products.products import DummyInMemoryProductRepository
from infrastructure.database.repositories.dummy.seo_settings.seo_settings import DummyInMemorySeoSettingsRepository
from infrastructure.database.repositories.dummy.submissions.submissions import DummyInMemorySubmissionRepository
from infrastructure.database.repositories.dummy.users.users import DummyInMemoryUserRepository
from infrastructure.database.repositories.dummy.vacancies.vacancies import DummyInMemoryVacancyRepository


def get_dummy_container() -> Container:
    container = _init_container()

    # Регистрируем dummy репозитории как синглтоны
    container.register(
        BaseUserRepository,
        DummyInMemoryUserRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseNewsRepository,
        DummyInMemoryNewsRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseVacancyRepository,
        DummyInMemoryVacancyRepository,
        scope=Scope.singleton,
    )
    container.register(
        BasePortfolioRepository,
        DummyInMemoryPortfolioRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseProductRepository,
        DummyInMemoryProductRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseSeoSettingsRepository,
        DummyInMemorySeoSettingsRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseCertificateGroupRepository,
        DummyInMemoryCertificateGroupRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseCertificateRepository,
        DummyInMemoryCertificateRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMemberRepository,
        DummyInMemoryMemberRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseSubmissionRepository,
        DummyInMemorySubmissionRepository,
        scope=Scope.singleton,
    )

    return container
