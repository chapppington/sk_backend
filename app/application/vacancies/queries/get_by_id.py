from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.services import VacancyService


@dataclass(frozen=True)
class GetVacancyByIdQuery(BaseQuery):
    vacancy_id: UUID


@dataclass(frozen=True)
class GetVacancyByIdQueryHandler(
    BaseQueryHandler[GetVacancyByIdQuery, VacancyEntity],
):
    vacancy_service: VacancyService

    async def handle(
        self,
        query: GetVacancyByIdQuery,
    ) -> VacancyEntity:
        return await self.vacancy_service.get_by_id(
            vacancy_id=query.vacancy_id,
        )
