from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.vacancies.entities import VacancyEntity
from domain.vacancies.exceptions import VacancyNotFoundException
from domain.vacancies.interfaces.repository import BaseVacancyRepository


@dataclass
class VacancyService:
    vacancy_repository: BaseVacancyRepository

    async def create(
        self,
        vacancy: VacancyEntity,
    ) -> VacancyEntity:
        await self.vacancy_repository.add(vacancy)

        return vacancy

    async def get_by_id(
        self,
        vacancy_id: UUID,
    ) -> VacancyEntity:
        vacancy = await self.vacancy_repository.get_by_id(vacancy_id)

        if not vacancy:
            raise VacancyNotFoundException(vacancy_id=vacancy_id)

        return vacancy

    async def update(
        self,
        vacancy: VacancyEntity,
    ) -> VacancyEntity:
        await self.vacancy_repository.update(vacancy)

        return vacancy

    async def delete(
        self,
        vacancy_id: UUID,
    ) -> None:
        await self.get_by_id(vacancy_id)
        await self.vacancy_repository.delete(vacancy_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        category: Optional[str] = None,
    ) -> list[VacancyEntity]:
        vacancies_iterable = self.vacancy_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
            category=category,
        )
        return [vacancy async for vacancy in vacancies_iterable]

    async def count_many(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
    ) -> int:
        return await self.vacancy_repository.count_many(
            search=search,
            category=category,
        )
