from fastapi import status

from domain.products.exceptions.products import (
    ProductAlreadyExistsException,
    ProductException,
    ProductNotFoundBySlugException,
    ProductNotFoundException,
)


def map_product_exception_to_status_code(exc: ProductException) -> int:
    if isinstance(exc, (ProductNotFoundException, ProductNotFoundBySlugException)):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, ProductAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
