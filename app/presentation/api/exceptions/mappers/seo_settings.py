from fastapi import status

from domain.seo_settings.exceptions.seo_settings import (
    SeoSettingsAlreadyExistsException,
    SeoSettingsException,
    SeoSettingsNotFoundByPathException,
    SeoSettingsNotFoundException,
)


def map_seo_settings_exception_to_status_code(exc: SeoSettingsException) -> int:
    if isinstance(exc, (SeoSettingsNotFoundException, SeoSettingsNotFoundByPathException)):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, SeoSettingsAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
