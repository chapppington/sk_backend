from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.interfaces.repository import BaseVacancyRepository


@dataclass
class DummyInMemoryVacancyRepository(BaseVacancyRepository):
    _saved_vacancies: list[VacancyEntity] = field(default_factory=list, kw_only=True)

    async def add(self, vacancy: VacancyEntity) -> VacancyEntity:
        self._saved_vacancies.append(vacancy)
        return vacancy

    async def get_by_id(self, vacancy_id: UUID) -> VacancyEntity | None:
        try:
            return next(vacancy for vacancy in self._saved_vacancies if vacancy.oid == vacancy_id)
        except StopIteration:
            return None

    async def update(self, vacancy: VacancyEntity) -> None:
        for i, saved_vacancy in enumerate(self._saved_vacancies):
            if saved_vacancy.oid == vacancy.oid:
                self._saved_vacancies[i] = vacancy
                return
        raise ValueError(f"Vacancy with id {vacancy.oid} not found")

    async def delete(self, vacancy_id: UUID) -> None:
        self._saved_vacancies = [vacancy for vacancy in self._saved_vacancies if vacancy.oid != vacancy_id]

    def _build_find_query(self, search: str | None = None, category: str | None = None) -> list[VacancyEntity]:
        filtered_vacancies = self._saved_vacancies.copy()

        if category:
            filtered_vacancies = [
                vacancy for vacancy in filtered_vacancies if vacancy.category.as_generic_type() == category
            ]

        if search:
            search_lower = search.lower()
            filtered_vacancies = [
                vacancy
                for vacancy in filtered_vacancies
                if (
                    search_lower in vacancy.title.as_generic_type().lower()
                    or any(search_lower in req.lower() for req in vacancy.requirements.as_generic_type())
                    or any(search_lower in exp.lower() for exp in vacancy.experience.as_generic_type())
                    or search_lower in vacancy.category.as_generic_type().lower()
                )
            ]

        return filtered_vacancies

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        category: str | None = None,
    ) -> AsyncIterable[VacancyEntity]:
        filtered_vacancies = self._build_find_query(search, category)

        reverse = sort_order == -1

        if sort_field == "created_at":
            filtered_vacancies.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "title":
            filtered_vacancies.sort(key=lambda x: x.title.as_generic_type(), reverse=reverse)
        elif sort_field == "category":
            filtered_vacancies.sort(key=lambda x: x.category.as_generic_type(), reverse=reverse)
        elif sort_field == "salary":
            filtered_vacancies.sort(key=lambda x: x.salary.as_generic_type(), reverse=reverse)
        else:
            filtered_vacancies.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_vacancies = filtered_vacancies[offset : offset + limit]

        for vacancy in paginated_vacancies:
            yield vacancy

    async def count_many(self, search: str | None = None, category: str | None = None) -> int:
        filtered_vacancies = self._build_find_query(search, category)
        return len(filtered_vacancies)
