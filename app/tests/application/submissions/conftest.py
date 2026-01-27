import pytest
from faker import Faker

from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.value_objects.submissions import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
    QuestionnaireTypeValueObject,
)


@pytest.fixture
def valid_submission_entity(faker: Faker) -> SubmissionEntity:
    return SubmissionEntity(
        form_type=FormTypeValueObject(value="Опросный лист"),
        name=NameValueObject(value=faker.name()),
        email=EmailValueObject(value=faker.email()),
        phone=PhoneValueObject(value=faker.phone_number()),
        comments=CommentsValueObject(value=faker.text(max_nb_chars=200)),
        questionnaire_type=QuestionnaireTypeValueObject(value="КТП"),
    )


@pytest.fixture
def valid_submission_entity_with_form_type(faker: Faker):
    def _create(form_type: str = "Опросный лист") -> SubmissionEntity:
        return SubmissionEntity(
            form_type=FormTypeValueObject(value=form_type),
            name=NameValueObject(value=faker.name()),
            email=EmailValueObject(value=faker.email()),
            phone=PhoneValueObject(value=faker.phone_number()),
            comments=CommentsValueObject(value=faker.text(max_nb_chars=200)),
        )

    return _create
