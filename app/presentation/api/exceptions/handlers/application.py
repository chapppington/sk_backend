from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse

from presentation.api.exceptions.mappers import map_domain_exception_to_status_code
from presentation.api.schemas import ApiResponse

from application.base.exception import LogicException
from domain.base.exceptions import (
    ApplicationException,
    DomainException,
)


def _map_application_exception_to_status_code(exc: ApplicationException) -> int:
    if isinstance(exc, LogicException):
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, DomainException):
        return map_domain_exception_to_status_code(exc)
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
