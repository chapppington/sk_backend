from fastapi import status

from domain.warehouse_file.exceptions.warehouse_file import WarehouseFileException


def map_warehouse_file_exception_to_status_code(
    exc: WarehouseFileException,
) -> int:
    return status.HTTP_400_BAD_REQUEST
