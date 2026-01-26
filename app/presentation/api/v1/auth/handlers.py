from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from application.container import init_container
from application.mediator import Mediator
from application.users.commands import CreateUserCommand
from application.users.queries import AuthenticateUserQuery
from presentation.api.auth import (
    create_and_set_access_token,
    create_and_set_refresh_token,
)
from presentation.api.dependencies import get_refresh_token_payload
from presentation.api.schemas import (
    ApiResponse,
    ErrorResponseSchema,
)
from presentation.api.v1.auth.schemas import (
    LoginRequestSchema,
    RefreshTokenResponseSchema,
    RegisterRequestSchema,
    TokenResponseSchema,
    UserResponseSchema,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[UserResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[UserResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def register(
    request: RegisterRequestSchema,
    container=Depends(init_container),
) -> ApiResponse[UserResponseSchema]:
    """Регистрация нового пользователя."""
    mediator: Mediator = container.resolve(Mediator)
    command = CreateUserCommand(
        email=request.email,
        password=request.password,
        name=request.name,
    )

    user, *_ = await mediator.handle_command(command)

    return ApiResponse[UserResponseSchema](
        data=UserResponseSchema.from_entity(user),
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[TokenResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[TokenResponseSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def login(
    request: LoginRequestSchema,
    response: Response,
    container=Depends(init_container),
) -> ApiResponse[TokenResponseSchema]:
    """Аутентификация пользователя и получение токенов."""
    mediator: Mediator = container.resolve(Mediator)

    query = AuthenticateUserQuery(
        email=request.email,
        password=request.password,
    )

    user = await mediator.handle_query(query)

    user_id = str(user.oid)
    access_token = create_and_set_access_token(user_id, response)
    refresh_token = create_and_set_refresh_token(user_id, response)

    return ApiResponse[TokenResponseSchema](
        data=TokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )


@router.post(
    "/token/refresh",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[RefreshTokenResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[RefreshTokenResponseSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
    },
)
async def refresh_token(
    response: Response,
    refresh_payload: dict = Depends(get_refresh_token_payload),
) -> ApiResponse[RefreshTokenResponseSchema]:
    """Обновление access токена с помощью refresh токена из cookies."""
    user_id = refresh_payload.sub
    access_token = create_and_set_access_token(user_id, response)

    return ApiResponse[RefreshTokenResponseSchema](
        data=RefreshTokenResponseSchema(
            access_token=access_token,
        ),
    )
