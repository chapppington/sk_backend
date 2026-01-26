from fastapi import status

from domain.certificates.exceptions.certificate_groups import (
    CertificateGroupAlreadyExistsException,
    CertificateGroupException,
    CertificateGroupNotFoundException,
)
from domain.certificates.exceptions.certificates import (
    CertificateAlreadyExistsException,
    CertificateException,
    CertificateNotFoundException,
)


def map_certificate_group_exception_to_status_code(exc: CertificateGroupException) -> int:
    if isinstance(exc, CertificateGroupNotFoundException):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, CertificateGroupAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def map_certificate_exception_to_status_code(exc: CertificateException) -> int:
    if isinstance(exc, CertificateNotFoundException):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, CertificateAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
