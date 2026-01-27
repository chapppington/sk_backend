from dataclasses import (
    dataclass,
    field,
)
from typing import Any

from domain.base.entity import BaseEntity
from domain.submissions.value_objects import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
    QuestionnaireTypeValueObject,
)


@dataclass(eq=False)
class SubmissionEntity(BaseEntity):
    form_type: FormTypeValueObject
    name: NameValueObject
    email: EmailValueObject | None = None
    phone: PhoneValueObject | None = None
    comments: CommentsValueObject | None = None
    files: list[str] = field(default_factory=list)
    questionnaire_answers: Any = None
    questionnaire_type: QuestionnaireTypeValueObject | None = None
