from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from application.certificates.commands import (
    CreateCertificateCommand,
    CreateCertificateCommandHandler,
    CreateCertificateGroupCommand,
    CreateCertificateGroupCommandHandler,
    DeleteCertificateCommand,
    DeleteCertificateCommandHandler,
    DeleteCertificateGroupCommand,
    DeleteCertificateGroupCommandHandler,
    PatchCertificateGroupOrderCommand,
    PatchCertificateGroupOrderCommandHandler,
    PatchCertificateOrderCommand,
    PatchCertificateOrderCommandHandler,
    UpdateCertificateCommand,
    UpdateCertificateCommandHandler,
    UpdateCertificateGroupCommand,
    UpdateCertificateGroupCommandHandler,
)
from application.certificates.queries import (
    GetCertificateByIdQuery,
    GetCertificateByIdQueryHandler,
    GetCertificateGroupByIdQuery,
    GetCertificateGroupByIdQueryHandler,
    GetCertificateGroupsListQuery,
    GetCertificateGroupsListQueryHandler,
    GetCertificatesListQuery,
    GetCertificatesListQueryHandler,
)
from application.media.commands import (
    UploadFileCommand,
    UploadFileCommandHandler,
)
from application.mediator import Mediator
from application.members.commands import (
    CreateMemberCommand,
    CreateMemberCommandHandler,
    DeleteMemberCommand,
    DeleteMemberCommandHandler,
    PatchMemberOrderCommand,
    PatchMemberOrderCommandHandler,
    UpdateMemberCommand,
    UpdateMemberCommandHandler,
)
from application.members.queries import (
    GetMemberByIdQuery,
    GetMemberByIdQueryHandler,
    GetMemberListQuery,
    GetMemberListQueryHandler,
)
from application.news.commands import (
    CreateNewsCommand,
    CreateNewsCommandHandler,
    DeleteNewsCommand,
    DeleteNewsCommandHandler,
    UpdateNewsCommand,
    UpdateNewsCommandHandler,
)
from application.news.queries import (
    GetNewsByIdQuery,
    GetNewsByIdQueryHandler,
    GetNewsBySlugQuery,
    GetNewsBySlugQueryHandler,
    GetNewsListQuery,
    GetNewsListQueryHandler,
)
from application.portfolios.commands import (
    CreatePortfolioCommand,
    CreatePortfolioCommandHandler,
    DeletePortfolioCommand,
    DeletePortfolioCommandHandler,
    UpdatePortfolioCommand,
    UpdatePortfolioCommandHandler,
)
from application.portfolios.queries import (
    GetPortfolioByIdQuery,
    GetPortfolioByIdQueryHandler,
    GetPortfolioBySlugQuery,
    GetPortfolioBySlugQueryHandler,
    GetPortfolioListQuery,
    GetPortfolioListQueryHandler,
)
from application.products.commands import (
    CreateProductCommand,
    CreateProductCommandHandler,
    DeleteProductCommand,
    DeleteProductCommandHandler,
    PatchProductOrderCommand,
    PatchProductOrderCommandHandler,
    UpdateProductCommand,
    UpdateProductCommandHandler,
)
from application.products.queries import (
    GetProductByIdQuery,
    GetProductByIdQueryHandler,
    GetProductBySlugQuery,
    GetProductBySlugQueryHandler,
    GetProductListQuery,
    GetProductListQueryHandler,
)
from application.reviews.commands import (
    CreateReviewCommand,
    CreateReviewCommandHandler,
    DeleteReviewCommand,
    DeleteReviewCommandHandler,
    UpdateReviewCommand,
    UpdateReviewCommandHandler,
)
from application.reviews.queries import (
    GetReviewByIdQuery,
    GetReviewByIdQueryHandler,
    GetReviewsListQuery,
    GetReviewsListQueryHandler,
)
from application.seo_settings.commands import (
    CreateSeoSettingsCommand,
    CreateSeoSettingsCommandHandler,
    DeleteSeoSettingsCommand,
    DeleteSeoSettingsCommandHandler,
    UpdateSeoSettingsCommand,
    UpdateSeoSettingsCommandHandler,
)
from application.seo_settings.queries import (
    GetSeoSettingsByIdQuery,
    GetSeoSettingsByIdQueryHandler,
    GetSeoSettingsByPathQuery,
    GetSeoSettingsByPathQueryHandler,
    GetSeoSettingsListQuery,
    GetSeoSettingsListQueryHandler,
)
from application.submissions.commands import (
    CreateSubmissionCommand,
    CreateSubmissionCommandHandler,
    DeleteSubmissionCommand,
    DeleteSubmissionCommandHandler,
)
from application.submissions.queries import (
    GetSubmissionByIdQuery,
    GetSubmissionByIdQueryHandler,
    GetSubmissionListQuery,
    GetSubmissionListQueryHandler,
)
from application.users.commands import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from application.users.queries import (
    AuthenticateUserQuery,
    AuthenticateUserQueryHandler,
    GetUserByIdQuery,
    GetUserByIdQueryHandler,
)
from application.vacancies.commands import (
    CreateVacancyCommand,
    CreateVacancyCommandHandler,
    DeleteVacancyCommand,
    DeleteVacancyCommandHandler,
    UpdateVacancyCommand,
    UpdateVacancyCommandHandler,
)
from application.vacancies.queries import (
    GetVacancyByIdQuery,
    GetVacancyByIdQueryHandler,
    GetVacancyListQuery,
    GetVacancyListQueryHandler,
)
from domain.certificates.interfaces.repositories.certificate_groups import BaseCertificateGroupRepository
from domain.certificates.interfaces.repositories.certificates import BaseCertificateRepository
from domain.certificates.services import (
    CertificateGroupService,
    CertificateService,
)
from domain.members.interfaces.repository import BaseMemberRepository
from domain.members.services import MemberService
from domain.news.interfaces.repository import BaseNewsRepository
from domain.news.services import NewsService
from domain.portfolios.interfaces.repository import BasePortfolioRepository
from domain.portfolios.services.portfolios import PortfolioService
from domain.products.interfaces.repository import BaseProductRepository
from domain.products.services import ProductService
from domain.reviews.interfaces.repository import BaseReviewRepository
from domain.reviews.services import ReviewService
from domain.seo_settings.interfaces.repository import BaseSeoSettingsRepository
from domain.seo_settings.services import SeoSettingsService
from domain.submissions.interfaces.repository import BaseSubmissionRepository
from domain.submissions.services import SubmissionService
from domain.users.interfaces.repository import BaseUserRepository
from domain.users.services import UserService
from domain.vacancies.interfaces.repository import BaseVacancyRepository
from domain.vacancies.services import VacancyService
from infrastructure.database.gateways.mongo import MongoDatabase
from infrastructure.database.repositories.certificates import (
    MongoCertificateGroupRepository,
    MongoCertificateRepository,
)
from infrastructure.database.repositories.members.mongo import MongoMemberRepository
from infrastructure.database.repositories.news.mongo import MongoNewsRepository
from infrastructure.database.repositories.portfolios.mongo import MongoPortfolioRepository
from infrastructure.database.repositories.products.mongo import MongoProductRepository
from infrastructure.database.repositories.reviews.mongo import MongoReviewRepository
from infrastructure.database.repositories.seo_settings.mongo import MongoSeoSettingsRepository
from infrastructure.database.repositories.submissions.mongo import MongoSubmissionRepository
from infrastructure.database.repositories.users.mongo import MongoUserRepository
from infrastructure.database.repositories.vacancies.mongo import MongoVacancyRepository
from infrastructure.s3.base import BaseFileStorage
from infrastructure.s3.client import S3Client
from infrastructure.s3.storage import S3FileStorage
from settings.config import Config


@lru_cache(1)
def get_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # Регистрируем конфиг
    config = Config()
    container.register(Config, instance=config, scope=Scope.singleton)

    # Регистрируем S3
    def init_s3_client() -> S3Client:
        return S3Client(config=config)

    container.register(S3Client, factory=init_s3_client, scope=Scope.singleton)

    def init_s3_file_storage() -> S3FileStorage:
        return S3FileStorage(s3_client=container.resolve(S3Client))

    container.register(BaseFileStorage, factory=init_s3_file_storage, scope=Scope.singleton)

    # Регистрируем Mongo Database
    def init_mongo_database() -> MongoDatabase:
        return MongoDatabase(mongo_url=config.mongo_connection_url, mongo_database=config.mongo_database)

    container.register(MongoDatabase, factory=init_mongo_database, scope=Scope.singleton)

    # Регистрируем репозитории
    container.register(BaseUserRepository, MongoUserRepository)
    container.register(BaseNewsRepository, MongoNewsRepository)
    container.register(BaseVacancyRepository, MongoVacancyRepository)
    container.register(BasePortfolioRepository, MongoPortfolioRepository)
    container.register(BaseProductRepository, MongoProductRepository)
    container.register(BaseSeoSettingsRepository, MongoSeoSettingsRepository)
    container.register(BaseCertificateGroupRepository, MongoCertificateGroupRepository)
    container.register(BaseCertificateRepository, MongoCertificateRepository)
    container.register(BaseMemberRepository, MongoMemberRepository)
    container.register(BaseReviewRepository, MongoReviewRepository)
    container.register(BaseSubmissionRepository, MongoSubmissionRepository)

    # Регистрируем доменные сервисы
    container.register(UserService)
    container.register(NewsService)
    container.register(VacancyService)
    container.register(PortfolioService)
    container.register(ProductService)
    container.register(SeoSettingsService)
    container.register(CertificateGroupService)
    container.register(CertificateService)
    container.register(MemberService)
    container.register(ReviewService)
    container.register(SubmissionService)

    # Регистрируем command handlers
    # Media
    container.register(UploadFileCommandHandler)
    # Users
    container.register(CreateUserCommandHandler)
    # News
    container.register(CreateNewsCommandHandler)
    container.register(UpdateNewsCommandHandler)
    container.register(DeleteNewsCommandHandler)
    # Vacancies
    container.register(CreateVacancyCommandHandler)
    container.register(UpdateVacancyCommandHandler)
    container.register(DeleteVacancyCommandHandler)
    # Submissions
    container.register(CreateSubmissionCommandHandler)
    container.register(DeleteSubmissionCommandHandler)
    # Portfolios
    container.register(CreatePortfolioCommandHandler)
    container.register(UpdatePortfolioCommandHandler)
    container.register(DeletePortfolioCommandHandler)
    # Products
    container.register(CreateProductCommandHandler)
    container.register(UpdateProductCommandHandler)
    container.register(PatchProductOrderCommandHandler)
    container.register(DeleteProductCommandHandler)
    # SEO Settings
    container.register(CreateSeoSettingsCommandHandler)
    container.register(UpdateSeoSettingsCommandHandler)
    container.register(DeleteSeoSettingsCommandHandler)
    # Certificates
    container.register(CreateCertificateGroupCommandHandler)
    container.register(UpdateCertificateGroupCommandHandler)
    container.register(PatchCertificateGroupOrderCommandHandler)
    container.register(DeleteCertificateGroupCommandHandler)
    container.register(CreateCertificateCommandHandler)
    container.register(UpdateCertificateCommandHandler)
    container.register(PatchCertificateOrderCommandHandler)
    container.register(DeleteCertificateCommandHandler)
    # Members
    container.register(CreateMemberCommandHandler)
    container.register(UpdateMemberCommandHandler)
    container.register(PatchMemberOrderCommandHandler)
    container.register(DeleteMemberCommandHandler)
    # Reviews
    container.register(CreateReviewCommandHandler)
    container.register(UpdateReviewCommandHandler)
    container.register(DeleteReviewCommandHandler)

    # Регистрируем query handlers
    # Users
    container.register(AuthenticateUserQueryHandler)
    container.register(GetUserByIdQueryHandler)
    # News
    container.register(GetNewsByIdQueryHandler)
    container.register(GetNewsBySlugQueryHandler)
    container.register(GetNewsListQueryHandler)
    # Vacancies
    container.register(GetVacancyByIdQueryHandler)
    container.register(GetVacancyListQueryHandler)
    # Members
    container.register(GetMemberByIdQueryHandler)
    container.register(GetMemberListQueryHandler)
    # Reviews
    container.register(GetReviewByIdQueryHandler)
    container.register(GetReviewsListQueryHandler)
    # Submissions
    container.register(GetSubmissionByIdQueryHandler)
    container.register(GetSubmissionListQueryHandler)
    # Portfolios
    container.register(GetPortfolioByIdQueryHandler)
    container.register(GetPortfolioBySlugQueryHandler)
    container.register(GetPortfolioListQueryHandler)
    # Products
    container.register(GetProductByIdQueryHandler)
    container.register(GetProductBySlugQueryHandler)
    container.register(GetProductListQueryHandler)
    # SEO Settings
    container.register(GetSeoSettingsByIdQueryHandler)
    container.register(GetSeoSettingsByPathQueryHandler)
    container.register(GetSeoSettingsListQueryHandler)
    # Certificates
    container.register(GetCertificateGroupByIdQueryHandler)
    container.register(GetCertificateGroupsListQueryHandler)
    container.register(GetCertificateByIdQueryHandler)
    container.register(GetCertificatesListQueryHandler)

    # Инициализируем медиатор
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Регистрируем commands
        # Media
        mediator.register_command(
            UploadFileCommand,
            [container.resolve(UploadFileCommandHandler)],
        )
        # Users
        mediator.register_command(
            CreateUserCommand,
            [container.resolve(CreateUserCommandHandler)],
        )
        # News
        mediator.register_command(
            CreateNewsCommand,
            [container.resolve(CreateNewsCommandHandler)],
        )
        mediator.register_command(
            UpdateNewsCommand,
            [container.resolve(UpdateNewsCommandHandler)],
        )
        mediator.register_command(
            DeleteNewsCommand,
            [container.resolve(DeleteNewsCommandHandler)],
        )
        # Vacancies
        mediator.register_command(
            CreateVacancyCommand,
            [container.resolve(CreateVacancyCommandHandler)],
        )
        mediator.register_command(
            UpdateVacancyCommand,
            [container.resolve(UpdateVacancyCommandHandler)],
        )
        mediator.register_command(
            DeleteVacancyCommand,
            [container.resolve(DeleteVacancyCommandHandler)],
        )
        # Submissions
        mediator.register_command(
            CreateSubmissionCommand,
            [container.resolve(CreateSubmissionCommandHandler)],
        )
        mediator.register_command(
            DeleteSubmissionCommand,
            [container.resolve(DeleteSubmissionCommandHandler)],
        )
        # Portfolios
        mediator.register_command(
            CreatePortfolioCommand,
            [container.resolve(CreatePortfolioCommandHandler)],
        )
        mediator.register_command(
            UpdatePortfolioCommand,
            [container.resolve(UpdatePortfolioCommandHandler)],
        )
        mediator.register_command(
            DeletePortfolioCommand,
            [container.resolve(DeletePortfolioCommandHandler)],
        )
        # Products
        mediator.register_command(
            CreateProductCommand,
            [container.resolve(CreateProductCommandHandler)],
        )
        mediator.register_command(
            UpdateProductCommand,
            [container.resolve(UpdateProductCommandHandler)],
        )
        mediator.register_command(
            PatchProductOrderCommand,
            [container.resolve(PatchProductOrderCommandHandler)],
        )
        mediator.register_command(
            DeleteProductCommand,
            [container.resolve(DeleteProductCommandHandler)],
        )
        # SEO Settings
        mediator.register_command(
            CreateSeoSettingsCommand,
            [container.resolve(CreateSeoSettingsCommandHandler)],
        )
        mediator.register_command(
            UpdateSeoSettingsCommand,
            [container.resolve(UpdateSeoSettingsCommandHandler)],
        )
        mediator.register_command(
            DeleteSeoSettingsCommand,
            [container.resolve(DeleteSeoSettingsCommandHandler)],
        )
        # Certificates
        mediator.register_command(
            CreateCertificateGroupCommand,
            [container.resolve(CreateCertificateGroupCommandHandler)],
        )
        mediator.register_command(
            UpdateCertificateGroupCommand,
            [container.resolve(UpdateCertificateGroupCommandHandler)],
        )
        mediator.register_command(
            PatchCertificateGroupOrderCommand,
            [container.resolve(PatchCertificateGroupOrderCommandHandler)],
        )
        mediator.register_command(
            DeleteCertificateGroupCommand,
            [container.resolve(DeleteCertificateGroupCommandHandler)],
        )
        mediator.register_command(
            CreateCertificateCommand,
            [container.resolve(CreateCertificateCommandHandler)],
        )
        mediator.register_command(
            UpdateCertificateCommand,
            [container.resolve(UpdateCertificateCommandHandler)],
        )
        mediator.register_command(
            PatchCertificateOrderCommand,
            [container.resolve(PatchCertificateOrderCommandHandler)],
        )
        mediator.register_command(
            DeleteCertificateCommand,
            [container.resolve(DeleteCertificateCommandHandler)],
        )
        # Members
        mediator.register_command(
            CreateMemberCommand,
            [container.resolve(CreateMemberCommandHandler)],
        )
        mediator.register_command(
            UpdateMemberCommand,
            [container.resolve(UpdateMemberCommandHandler)],
        )
        mediator.register_command(
            PatchMemberOrderCommand,
            [container.resolve(PatchMemberOrderCommandHandler)],
        )
        mediator.register_command(
            DeleteMemberCommand,
            [container.resolve(DeleteMemberCommandHandler)],
        )
        # Reviews
        mediator.register_command(
            CreateReviewCommand,
            [container.resolve(CreateReviewCommandHandler)],
        )
        mediator.register_command(
            UpdateReviewCommand,
            [container.resolve(UpdateReviewCommandHandler)],
        )
        mediator.register_command(
            DeleteReviewCommand,
            [container.resolve(DeleteReviewCommandHandler)],
        )

        # Регистрируем queries
        # Users
        mediator.register_query(
            AuthenticateUserQuery,
            container.resolve(AuthenticateUserQueryHandler),
        )
        mediator.register_query(
            GetUserByIdQuery,
            container.resolve(GetUserByIdQueryHandler),
        )
        # News
        mediator.register_query(
            GetNewsByIdQuery,
            container.resolve(GetNewsByIdQueryHandler),
        )
        mediator.register_query(
            GetNewsBySlugQuery,
            container.resolve(GetNewsBySlugQueryHandler),
        )
        mediator.register_query(
            GetNewsListQuery,
            container.resolve(GetNewsListQueryHandler),
        )
        # Vacancies
        mediator.register_query(
            GetVacancyByIdQuery,
            container.resolve(GetVacancyByIdQueryHandler),
        )
        mediator.register_query(
            GetVacancyListQuery,
            container.resolve(GetVacancyListQueryHandler),
        )
        # Members
        mediator.register_query(
            GetMemberByIdQuery,
            container.resolve(GetMemberByIdQueryHandler),
        )
        mediator.register_query(
            GetMemberListQuery,
            container.resolve(GetMemberListQueryHandler),
        )
        # Reviews
        mediator.register_query(
            GetReviewByIdQuery,
            container.resolve(GetReviewByIdQueryHandler),
        )
        mediator.register_query(
            GetReviewsListQuery,
            container.resolve(GetReviewsListQueryHandler),
        )
        # Submissions
        mediator.register_query(
            GetSubmissionByIdQuery,
            container.resolve(GetSubmissionByIdQueryHandler),
        )
        mediator.register_query(
            GetSubmissionListQuery,
            container.resolve(GetSubmissionListQueryHandler),
        )
        # Portfolios
        mediator.register_query(
            GetPortfolioByIdQuery,
            container.resolve(GetPortfolioByIdQueryHandler),
        )
        mediator.register_query(
            GetPortfolioBySlugQuery,
            container.resolve(GetPortfolioBySlugQueryHandler),
        )
        mediator.register_query(
            GetPortfolioListQuery,
            container.resolve(GetPortfolioListQueryHandler),
        )
        # Products
        mediator.register_query(
            GetProductByIdQuery,
            container.resolve(GetProductByIdQueryHandler),
        )
        mediator.register_query(
            GetProductBySlugQuery,
            container.resolve(GetProductBySlugQueryHandler),
        )
        mediator.register_query(
            GetProductListQuery,
            container.resolve(GetProductListQueryHandler),
        )
        # SEO Settings
        mediator.register_query(
            GetSeoSettingsByIdQuery,
            container.resolve(GetSeoSettingsByIdQueryHandler),
        )
        mediator.register_query(
            GetSeoSettingsByPathQuery,
            container.resolve(GetSeoSettingsByPathQueryHandler),
        )
        mediator.register_query(
            GetSeoSettingsListQuery,
            container.resolve(GetSeoSettingsListQueryHandler),
        )
        # Certificates
        mediator.register_query(
            GetCertificateGroupByIdQuery,
            container.resolve(GetCertificateGroupByIdQueryHandler),
        )
        mediator.register_query(
            GetCertificateGroupsListQuery,
            container.resolve(GetCertificateGroupsListQueryHandler),
        )
        mediator.register_query(
            GetCertificateByIdQuery,
            container.resolve(GetCertificateByIdQueryHandler),
        )
        mediator.register_query(
            GetCertificatesListQuery,
            container.resolve(GetCertificatesListQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
