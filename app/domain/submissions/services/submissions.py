from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.submissions.entities import SubmissionEntity
from domain.submissions.exceptions import SubmissionNotFoundException
from domain.submissions.interfaces.repository import BaseSubmissionRepository


@dataclass
class SubmissionService:
    submission_repository: BaseSubmissionRepository

    async def create(
        self,
        submission: SubmissionEntity,
    ) -> SubmissionEntity:
        await self.submission_repository.add(submission)
        return submission

    async def get_by_id(
        self,
        submission_id: UUID,
    ) -> SubmissionEntity:
        submission = await self.submission_repository.get_by_id(submission_id)

        if not submission:
            raise SubmissionNotFoundException(submission_id=submission_id)

        return submission

    async def delete(
        self,
        submission_id: UUID,
    ) -> None:
        await self.get_by_id(submission_id)
        await self.submission_repository.delete(submission_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        form_type: Optional[str] = None,
    ) -> list[SubmissionEntity]:
        submissions_iterable = self.submission_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            form_type=form_type,
        )
        return [submission async for submission in submissions_iterable]

    async def count_many(
        self,
        form_type: Optional[str] = None,
    ) -> int:
        return await self.submission_repository.count_many(form_type=form_type)
