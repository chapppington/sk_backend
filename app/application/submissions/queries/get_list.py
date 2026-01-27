import asyncio
from dataclasses import dataclass
from typing import Optional

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.services import SubmissionService


@dataclass(frozen=True)
class GetSubmissionListQuery(BaseQuery):
    sort_field: str
    sort_order: int
    offset: int
    limit: int
    form_type: Optional[str] = None


@dataclass(frozen=True)
class GetSubmissionListQueryHandler(
    BaseQueryHandler[GetSubmissionListQuery, tuple[list[SubmissionEntity], int]],
):
    submission_service: SubmissionService

    async def handle(
        self,
        query: GetSubmissionListQuery,
    ) -> tuple[list[SubmissionEntity], int]:
        submissions_task = asyncio.create_task(
            self.submission_service.find_many(
                sort_field=query.sort_field,
                sort_order=query.sort_order,
                offset=query.offset,
                limit=query.limit,
                form_type=query.form_type,
            ),
        )
        count_task = asyncio.create_task(
            self.submission_service.count_many(
                form_type=query.form_type,
            ),
        )

        return await submissions_task, await count_task
