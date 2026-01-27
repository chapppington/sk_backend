from fastapi import status

from domain.submissions.exceptions.submissions import (
    SubmissionException,
    SubmissionNotFoundException,
)


def map_submission_exception_to_status_code(exc: SubmissionException) -> int:
    if isinstance(exc, SubmissionNotFoundException):
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST
