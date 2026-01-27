from fastapi import Response

from authx import (
    AuthX,
    AuthXConfig,
)

from application.container import get_container
from settings.config import Config


container = get_container()
config = container.resolve(Config)

auth_config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=config.jwt_secret_key,
    JWT_TOKEN_LOCATION=["cookies", "headers"],
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_REFRESH_COOKIE_NAME="refresh_token",
    JWT_HEADER_NAME="Authorization",
    JWT_HEADER_TYPE="Bearer",
    JWT_COOKIE_CSRF_PROTECT=False,
    JWT_COOKIE_SAMESITE="lax",
    JWT_COOKIE_SECURE=False,
)

auth_service = AuthX(config=auth_config)


def create_and_set_access_token(user_id: str, response: Response) -> str:
    access_token = auth_service.create_access_token(uid=user_id)
    auth_service.set_access_cookies(token=access_token, response=response)
    return access_token


def create_and_set_refresh_token(user_id: str, response: Response) -> str:
    refresh_token = auth_service.create_refresh_token(uid=user_id)
    auth_service.set_refresh_cookies(token=refresh_token, response=response)
    return refresh_token
