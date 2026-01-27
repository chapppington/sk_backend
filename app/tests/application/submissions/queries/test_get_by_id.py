from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.submissions.commands import CreateSubmissionCommand
from application.submissions.queries import GetSubmissionByIdQuery
from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.exceptions.submissions import SubmissionNotFoundException


@pytest.mark.asyncio
async def test_get_submission_by_id_success(
    mediator: Mediator,
    valid_submission_entity: SubmissionEntity,
):
    create_result, *_ = await mediator.handle_command(
        CreateSubmissionCommand(submission=valid_submission_entity),
    )
    created_submission: SubmissionEntity = create_result

    retrieved_submission = await mediator.handle_query(
        GetSubmissionByIdQuery(submission_id=created_submission.oid),
    )

    assert retrieved_submission.oid == created_submission.oid
    assert retrieved_submission.form_type.as_generic_type() == valid_submission_entity.form_type.as_generic_type()
    assert retrieved_submission.name.as_generic_type() == valid_submission_entity.name.as_generic_type()


@pytest.mark.asyncio
async def test_get_submission_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(SubmissionNotFoundException) as exc_info:
        await mediator.handle_query(
            GetSubmissionByIdQuery(submission_id=non_existent_id),
        )

    assert exc_info.value.submission_id == non_existent_id
