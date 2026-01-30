import pytest

from application.mediator import Mediator
from application.submissions.commands import CreateSubmissionCommand
from application.submissions.queries import GetSubmissionByIdQuery
from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.value_objects.submissions import (
    FormTypeValueObject,
    NameValueObject,
)


@pytest.mark.asyncio
async def test_create_submission_command_success(
    mediator: Mediator,
    valid_submission_entity: SubmissionEntity,
):
    command = CreateSubmissionCommand(submission=valid_submission_entity)
    result, *_ = await mediator.handle_command(command)

    submission: SubmissionEntity = result

    assert submission is not None
    assert submission.form_type.as_generic_type() == valid_submission_entity.form_type.as_generic_type()
    assert submission.name.as_generic_type() == valid_submission_entity.name.as_generic_type()
    assert submission.email.as_generic_type() == valid_submission_entity.email.as_generic_type()
    assert submission.phone.as_generic_type() == valid_submission_entity.phone.as_generic_type()
    assert submission.comments.as_generic_type() == valid_submission_entity.comments.as_generic_type()
    assert submission.oid is not None

    retrieved_submission = await mediator.handle_query(
        GetSubmissionByIdQuery(submission_id=submission.oid),
    )

    assert retrieved_submission.oid == submission.oid
    assert retrieved_submission.form_type.as_generic_type() == valid_submission_entity.form_type.as_generic_type()


@pytest.mark.asyncio
async def test_create_submission_command_minimal(
    mediator: Mediator,
):
    minimal_submission = SubmissionEntity(
        form_type=FormTypeValueObject(value="Обращение"),
        name=NameValueObject(value="Иван Иванов"),
    )

    command = CreateSubmissionCommand(submission=minimal_submission)
    result, *_ = await mediator.handle_command(command)

    submission: SubmissionEntity = result

    assert submission is not None
    assert submission.form_type.as_generic_type() == "Обращение"
    assert submission.name.as_generic_type() == "Иван Иванов"
    assert submission.email is None
    assert submission.phone is None
    assert submission.comments is None
