from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse

from presentation.api.schemas import ApiResponse


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
