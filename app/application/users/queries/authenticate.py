from dataclasses import dataclass

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.users.entities import UserEntity
from domain.users.services import UserService


@dataclass(frozen=True)
class AuthenticateUserQuery(BaseQuery):
    email: str
    password: str


@dataclass(frozen=True)
class AuthenticateUserQueryHandler(
    BaseQueryHandler[AuthenticateUserQuery, UserEntity],
):
    user_service: UserService

    async def handle(
        self,
        query: AuthenticateUserQuery,
    ) -> UserEntity:
        return await self.user_service.authenticate_user(
            email=query.email,
            password=query.password,
        )
