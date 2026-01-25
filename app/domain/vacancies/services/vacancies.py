from dataclasses import dataclass
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
        existing_vacancy = await self.vacancy_repository.get_by_id(vacancy.oid)

        if not existing_vacancy:
            raise VacancyNotFoundException(vacancy_id=vacancy.oid)

        await self.vacancy_repository.update(vacancy)

        return vacancy

    async def delete(
        self,
        vacancy_id: UUID,
    ) -> None:
        await self.get_by_id(vacancy_id)
        await self.vacancy_repository.delete(vacancy_id)
