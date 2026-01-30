from dataclasses import (
    dataclass,
    field,
)

from domain.base.entity import BaseEntity
from domain.submissions.value_objects import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
)


@dataclass(eq=False)
class SubmissionEntity(BaseEntity):
    form_type: FormTypeValueObject
    name: NameValueObject
    email: EmailValueObject | None = None
    phone: PhoneValueObject | None = None
    comments: CommentsValueObject | None = None
    files: list[str] = field(default_factory=list)
    answers_file_url: str | None = None
