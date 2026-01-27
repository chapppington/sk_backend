import pytest

from application.mediator import Mediator
from application.submissions.commands import CreateSubmissionCommand
from application.submissions.queries import GetSubmissionListQuery
from domain.submissions.entities.submissions import SubmissionEntity


@pytest.mark.asyncio
async def test_get_submission_list_query_success(
    mediator: Mediator,
    valid_submission_entity_with_form_type,
):
    for _ in range(5):
        submission = valid_submission_entity_with_form_type("Опросный лист")
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    submission_list, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(submission_list) == 5
    assert total == 5
    assert all(isinstance(submission, SubmissionEntity) for submission in submission_list)


@pytest.mark.asyncio
async def test_get_submission_list_query_with_pagination(
    mediator: Mediator,
    valid_submission_entity_with_form_type,
):
    for _ in range(5):
        submission = valid_submission_entity_with_form_type()
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    submission_list, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(submission_list) == 2
    assert total == 5

    submission_list, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(submission_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_submission_list_query_with_form_type_filter(
    mediator: Mediator,
    valid_submission_entity_with_form_type,
):
    for _ in range(3):
        submission = valid_submission_entity_with_form_type("Опросный лист")
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    for _ in range(2):
        submission = valid_submission_entity_with_form_type("Отклик на вакансию")
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    submission_list, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            form_type="Опросный лист",
        ),
    )

    assert len(submission_list) == 3
    assert total == 3
    assert all(submission.form_type.as_generic_type() == "Опросный лист" for submission in submission_list)


@pytest.mark.asyncio
async def test_get_submission_list_query_with_sorting(
    mediator: Mediator,
    valid_submission_entity_with_form_type,
):
    submission1 = valid_submission_entity_with_form_type("Обращение")
    from domain.submissions.value_objects.submissions import NameValueObject

    submission1 = SubmissionEntity(
        form_type=submission1.form_type,
        name=NameValueObject(value="Алексей"),
        email=submission1.email,
        phone=submission1.phone,
        comments=submission1.comments,
    )
    await mediator.handle_command(
        CreateSubmissionCommand(submission=submission1),
    )

    submission2 = valid_submission_entity_with_form_type("Обращение")
    submission2 = SubmissionEntity(
        form_type=submission2.form_type,
        name=NameValueObject(value="Борис"),
        email=submission2.email,
        phone=submission2.phone,
        comments=submission2.comments,
    )
    await mediator.handle_command(
        CreateSubmissionCommand(submission=submission2),
    )

    submission_list, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="name",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(submission_list) == 2
    assert total == 2
    assert submission_list[0].name.as_generic_type() < submission_list[1].name.as_generic_type()


@pytest.mark.asyncio
async def test_get_submission_list_query_count_only(
    mediator: Mediator,
    valid_submission_entity_with_form_type,
):
    for _ in range(3):
        submission = valid_submission_entity_with_form_type()
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    _, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_submission_list_query_count_with_form_type(
    mediator: Mediator,
    valid_submission_entity_with_form_type,
):
    for _ in range(3):
        submission = valid_submission_entity_with_form_type("Опросный лист")
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    for _ in range(2):
        submission = valid_submission_entity_with_form_type("Обращение")
        await mediator.handle_command(
            CreateSubmissionCommand(submission=submission),
        )

    _, total = await mediator.handle_query(
        GetSubmissionListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            form_type="Опросный лист",
        ),
    )

    assert total == 3
