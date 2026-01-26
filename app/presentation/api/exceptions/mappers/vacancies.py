from fastapi import status

from domain.vacancies.exceptions.vacancies import (
    VacancyAlreadyExistsException,
    VacancyException,
    VacancyNotFoundException,
)


def map_vacancy_exception_to_status_code(exc: VacancyException) -> int:
    if isinstance(exc, VacancyNotFoundException):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, VacancyAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
