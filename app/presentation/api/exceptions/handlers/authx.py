from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse

from authx.exceptions import (
    JWTDecodeError,
    MissingTokenError,
)

from presentation.api.schemas import ApiResponse


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
