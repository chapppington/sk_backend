from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.vacancies.interfaces.repository import BaseVacancyRepository


@dataclass(frozen=True)
class CountManyVacanciesQuery(BaseQuery):
    search: Optional[str] = None
    category: Optional[str] = None


@dataclass(frozen=True)
class CountManyVacanciesQueryHandler(
    BaseQueryHandler[CountManyVacanciesQuery, int],
):
    vacancy_repository: BaseVacancyRepository

    async def handle(
        self,
        query: CountManyVacanciesQuery,
    ) -> int:
        return await self.vacancy_repository.count_many(
            search=query.search,
            category=query.category,
        )
