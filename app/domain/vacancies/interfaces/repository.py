from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.vacancies.entities import VacancyEntity


class BaseVacancyRepository(ABC):
    @abstractmethod
    async def add(self, vacancy: VacancyEntity) -> VacancyEntity: ...

    @abstractmethod
    async def get_by_id(self, vacancy_id: UUID) -> VacancyEntity | None: ...

    @abstractmethod
    async def update(self, vacancy: VacancyEntity) -> None: ...

    @abstractmethod
    async def delete(self, vacancy_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        category: str | None = None,
    ) -> AsyncIterable[VacancyEntity]: ...

    @abstractmethod
    async def count_many(self, search: str | None = None, category: str | None = None) -> int: ...
