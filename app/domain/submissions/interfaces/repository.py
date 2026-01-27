from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import AsyncIterable
from uuid import UUID

from domain.submissions.entities import SubmissionEntity


class BaseSubmissionRepository(ABC):
    @abstractmethod
    async def add(self, submission: SubmissionEntity) -> SubmissionEntity: ...

    @abstractmethod
    async def get_by_id(self, submission_id: UUID) -> SubmissionEntity | None: ...

    @abstractmethod
    async def delete(self, submission_id: UUID) -> None: ...

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        form_type: str | None = None,
    ) -> AsyncIterable[SubmissionEntity]: ...

    @abstractmethod
    async def count_many(self, form_type: str | None = None) -> int: ...
