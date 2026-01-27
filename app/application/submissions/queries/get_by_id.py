from dataclasses import dataclass
from uuid import UUID

from application.base.query import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.services import SubmissionService


@dataclass(frozen=True)
class GetSubmissionByIdQuery(BaseQuery):
    submission_id: UUID


@dataclass(frozen=True)
class GetSubmissionByIdQueryHandler(
    BaseQueryHandler[GetSubmissionByIdQuery, SubmissionEntity],
):
    submission_service: SubmissionService

    async def handle(
        self,
        query: GetSubmissionByIdQuery,
    ) -> SubmissionEntity:
        return await self.submission_service.get_by_id(
            submission_id=query.submission_id,
        )
