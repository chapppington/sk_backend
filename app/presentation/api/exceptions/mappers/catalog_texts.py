from fastapi import status

from domain.catalog_texts.exceptions.catalog_texts import (
    CatalogTextException,
    CatalogTextNotFoundException,
)


def map_catalog_text_exception_to_status_code(exc: CatalogTextException) -> int:
    if isinstance(exc, CatalogTextNotFoundException):
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST
