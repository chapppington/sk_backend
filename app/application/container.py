from functools import lru_cache

from infrastructure.database.gateways.mongo import MongoDatabase
from infrastructure.database.repositories.users.mongo import MongoUserRepository
from infrastructure.s3.base import BaseFileStorage
from infrastructure.s3.client import S3Client
from infrastructure.s3.storage import S3FileStorage
from punq import (
    Container,
    Scope,
)

from application.media.commands import (
    UploadFileCommand,
    UploadFileCommandHandler,
)
from application.mediator import Mediator
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
from domain.users.interfaces.repository import BaseUserRepository
from domain.users.services import UserService
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # Регистрируем конфиг
    config = Config()
    container.register(Config, instance=config, scope=Scope.singleton)

    # Регистрируем Mongo Database
    def init_mongo_database() -> MongoDatabase:
        return MongoDatabase(mongo_url=config.mongo_connection_url, mongo_database=config.mongo_database)

    container.register(MongoDatabase, factory=init_mongo_database, scope=Scope.singleton)

    container.register(BaseUserRepository, MongoUserRepository)

    # Регистрируем S3
    def init_s3_client() -> S3Client:
        return S3Client(config=config)

    container.register(S3Client, factory=init_s3_client, scope=Scope.singleton)

    def init_s3_file_storage() -> S3FileStorage:
        return S3FileStorage(s3_client=container.resolve(S3Client))

    container.register(BaseFileStorage, factory=init_s3_file_storage, scope=Scope.singleton)

    # Регистрируем доменные сервисы
    container.register(UserService)

    # Регистрируем command handlers
    # Media
    container.register(UploadFileCommandHandler)
    # Users
    container.register(CreateUserCommandHandler)

    # Регистрируем query handlers
    # Users
    container.register(AuthenticateUserQueryHandler)
    container.register(GetUserByIdQueryHandler)

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

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
