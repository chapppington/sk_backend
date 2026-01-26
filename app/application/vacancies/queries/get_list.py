import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.vacancies.entities import VacancyEntity
from domain.vacancies.services import VacancyService


@dataclass(frozen=True)
class GetVacancyListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    category: Optional[str] = None


@dataclass(frozen=True)
class GetVacancyListQueryHandler(
    BaseQueryHandler[GetVacancyListQuery, tuple[list[VacancyEntity], int]],
):
    vacancy_service: VacancyService

    async def handle(
        self,
        query: GetVacancyListQuery,
    ) -> tuple[list[VacancyEntity], int]:
        vacancies_task = asyncio.create_task(
            self.vacancy_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                search=query.search,
                category=query.category,
            ),
        )
        count_task = asyncio.create_task(
            self.vacancy_service.count_many(
                search=query.search,
                category=query.category,
            ),
        )

        return await vacancies_task, await count_task
