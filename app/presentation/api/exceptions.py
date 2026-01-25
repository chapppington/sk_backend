from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from authx.exceptions import (
    JWTDecodeError,
    MissingTokenError,
)
from presentation.api.schemas import ApiResponse

from application.base.exception import LogicException
from domain.base.exceptions import (
    ApplicationException,
    DomainException,
)
from domain.news.exceptions.news import (
    NewsAlreadyExistsException,
    NewsException,
    NewsNotFoundBySlugException,
    NewsNotFoundException,
)
from domain.users.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserException,
    UserNotFoundException,
)


def _map_user_exception_to_status_code(exc: UserException) -> int:
    if isinstance(exc, (InvalidCredentialsException, UserNotFoundException)):
        return status.HTTP_401_UNAUTHORIZED
    if isinstance(exc, UserAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def _map_news_exception_to_status_code(exc: NewsException) -> int:
    if isinstance(exc, (NewsNotFoundException, NewsNotFoundBySlugException)):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, NewsAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def _map_domain_exception_to_status_code(exc: DomainException) -> int:
    if isinstance(exc, UserException):
        return _map_user_exception_to_status_code(exc)
    if isinstance(exc, NewsException):
        return _map_news_exception_to_status_code(exc)
    return status.HTTP_400_BAD_REQUEST


def _map_application_exception_to_status_code(exc: ApplicationException) -> int:
    if isinstance(exc, LogicException):
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, DomainException):
        return _map_domain_exception_to_status_code(exc)
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def _create_error_response(exc: ApplicationException, status_code: int) -> JSONResponse:
    response = ApiResponse(
        errors=[{"message": exc.message, "type": exc.__class__.__name__}],
    )

    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(),
    )


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
) -> JSONResponse:
    status_code = _map_application_exception_to_status_code(exc)
    return _create_error_response(exc, status_code)


async def authx_exception_handler(
    request: Request,
    exc: MissingTokenError | JWTDecodeError,
) -> JSONResponse:
    response = ApiResponse(
        errors=[{"message": str(exc), "type": exc.__class__.__name__}],
    )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=response.model_dump(),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        loc = " -> ".join(str(loc) for loc in error.get("loc", []))
        msg = error.get("msg", "Validation error")
        error_type = error.get("type", "validation_error")
        errors.append(
            {
                "message": f"{loc}: {msg}",
                "type": error_type,
            },
        )

    response = ApiResponse(
        errors=errors,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump(),
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    response = ApiResponse(
        errors=[{"message": str(exc), "type": exc.__class__.__name__}],
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(),
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.add_exception_handler(
        ApplicationException,
        application_exception_handler,
    )
    app.add_exception_handler(
        MissingTokenError,
        authx_exception_handler,
    )
    app.add_exception_handler(
        JWTDecodeError,
        authx_exception_handler,
    )
    app.add_exception_handler(
        Exception,
        general_exception_handler,
    )
