from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from authx.exceptions import (
    JWTDecodeError,
    MissingTokenError,
)
from presentation.api.exceptions.handlers import (
    application_exception_handler,
    authx_exception_handler,
    general_exception_handler,
    validation_exception_handler,
)

from application.base.exception import ApplicationException


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
