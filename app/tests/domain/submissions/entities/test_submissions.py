from domain.submissions.entities import SubmissionEntity
from domain.submissions.value_objects.submissions import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
)


def test_submission_entity_creation():
    form_type = FormTypeValueObject("Опросный лист")
    name = NameValueObject("Иван Иванов")
    email = EmailValueObject("ivan@example.com")
    phone = PhoneValueObject("+7 (999) 123-45-67")
    comments = CommentsValueObject("Тестовый комментарий")

    submission = SubmissionEntity(
        form_type=form_type,
        name=name,
        email=email,
        phone=phone,
        comments=comments,
    )

    assert submission.form_type.as_generic_type() == "Опросный лист"
    assert submission.name.as_generic_type() == "Иван Иванов"
    assert submission.email.as_generic_type() == "ivan@example.com"
    assert submission.phone.as_generic_type() == "+7 (999) 123-45-67"
    assert submission.comments.as_generic_type() == "Тестовый комментарий"
    assert submission.files == []
    assert submission.answers_file_url is None
    assert submission.oid is not None
    assert submission.created_at is not None
    assert submission.updated_at is not None


def test_submission_entity_creation_minimal():
    form_type = FormTypeValueObject("Обращение")
    name = NameValueObject("Петр Петров")

    submission = SubmissionEntity(
        form_type=form_type,
        name=name,
    )

    assert submission.form_type.as_generic_type() == "Обращение"
    assert submission.name.as_generic_type() == "Петр Петров"
    assert submission.email is None
    assert submission.phone is None
    assert submission.comments is None
    assert submission.files == []
    assert submission.answers_file_url is None
    assert submission.oid is not None


def test_submission_entity_creation_with_files():
    form_type = FormTypeValueObject("Отклик на вакансию")
    name = NameValueObject("Мария Сидорова")
    files = ["file1.pdf", "file2.doc", "resume.pdf"]

    submission = SubmissionEntity(
        form_type=form_type,
        name=name,
        files=files,
    )

    assert submission.files == files
    assert len(submission.files) == 3


def test_submission_entity_creation_with_answers_file_url():
    form_type = FormTypeValueObject("Опросный лист")
    name = NameValueObject("Алексей Смирнов")
    answers_file_url = "https://storage.example.com/answers/file123.pdf"

    submission = SubmissionEntity(
        form_type=form_type,
        name=name,
        answers_file_url=answers_file_url,
    )

    assert submission.answers_file_url == answers_file_url
