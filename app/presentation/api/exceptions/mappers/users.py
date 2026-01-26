from fastapi import status

from domain.users.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserException,
    UserNotFoundException,
)


def map_user_exception_to_status_code(exc: UserException) -> int:
    if isinstance(exc, (InvalidCredentialsException, UserNotFoundException)):
        return status.HTTP_401_UNAUTHORIZED
    if isinstance(exc, UserAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
