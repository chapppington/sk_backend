from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.interfaces.repository import BaseSubmissionRepository


@dataclass
class DummyInMemorySubmissionRepository(BaseSubmissionRepository):
    _saved_submissions: list[SubmissionEntity] = field(default_factory=list, kw_only=True)

    async def add(self, submission: SubmissionEntity) -> SubmissionEntity:
        self._saved_submissions.append(submission)
        return submission

    async def get_by_id(self, submission_id: UUID) -> SubmissionEntity | None:
        try:
            return next(submission for submission in self._saved_submissions if submission.oid == submission_id)
        except StopIteration:
            return None

    async def delete(self, submission_id: UUID) -> None:
        self._saved_submissions = [
            submission for submission in self._saved_submissions if submission.oid != submission_id
        ]

    def _build_find_query(self, form_type: str | None = None) -> list[SubmissionEntity]:
        filtered_submissions = self._saved_submissions.copy()

        if form_type:
            filtered_submissions = [
                submission for submission in filtered_submissions if submission.form_type.as_generic_type() == form_type
            ]

        return filtered_submissions

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        form_type: str | None = None,
    ) -> AsyncIterable[SubmissionEntity]:
        filtered_submissions = self._build_find_query(form_type)

        reverse = sort_order == -1

        if sort_field == "created_at":
            filtered_submissions.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "name":
            filtered_submissions.sort(key=lambda x: x.name.as_generic_type(), reverse=reverse)
        elif sort_field == "form_type":
            filtered_submissions.sort(key=lambda x: x.form_type.as_generic_type(), reverse=reverse)
        else:
            filtered_submissions.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_submissions = filtered_submissions[offset : offset + limit]

        for submission in paginated_submissions:
            yield submission

    async def count_many(self, form_type: str | None = None) -> int:
        filtered_submissions = self._build_find_query(form_type)
        return len(filtered_submissions)
