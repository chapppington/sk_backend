from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.interfaces.repository import BaseVacancyRepository


@dataclass(frozen=True)
class FindManyVacanciesQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    search: Optional[str] = None
    category: Optional[str] = None


@dataclass(frozen=True)
class FindManyVacanciesQueryHandler(
    BaseQueryHandler[FindManyVacanciesQuery, list[VacancyEntity]],
):
    vacancy_repository: BaseVacancyRepository

    async def handle(
        self,
        query: FindManyVacanciesQuery,
    ) -> list[VacancyEntity]:
        vacancies_iterable = self.vacancy_repository.find_many(
            sort_field=query.sort_field,
            sort_order=query.sort_order,
            offset=query.offset,
            limit=query.limit,
            search=query.search,
            category=query.category,
        )
        return [vacancy async for vacancy in vacancies_iterable]
