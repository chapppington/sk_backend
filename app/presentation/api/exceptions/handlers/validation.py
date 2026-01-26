from fastapi import (
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from presentation.api.schemas import ApiResponse


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
