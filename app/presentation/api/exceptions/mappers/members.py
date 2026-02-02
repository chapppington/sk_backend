from fastapi import status

from domain.members.exceptions.members import (
    MemberException,
    MemberNotFoundException,
)


def map_member_exception_to_status_code(exc: MemberException) -> int:
    if isinstance(exc, MemberNotFoundException):
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST
