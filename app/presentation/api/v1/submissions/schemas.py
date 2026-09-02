from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    field_validator,
)

from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.value_objects.submissions import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
)


class SubmissionResponseSchema(BaseModel):
    oid: UUID
    form_type: str
    name: str
    email: str | None
    phone: str | None
    comments: str | None
    files: list[str]
    answers_file_url: str | None
    consent: bool
    marketing_consent: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: SubmissionEntity) -> "SubmissionResponseSchema":
        return cls(
            oid=entity.oid,
            form_type=entity.form_type.as_generic_type(),
            name=entity.name.as_generic_type(),
            email=entity.email.as_generic_type() if entity.email else None,
            phone=entity.phone.as_generic_type() if entity.phone else None,
            comments=entity.comments.as_generic_type() if entity.comments else None,
            files=entity.files,
            answers_file_url=entity.answers_file_url,
            consent=entity.consent,
            marketing_consent=entity.marketing_consent,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class SubmissionRequestSchema(BaseModel):
    form_type: str
    name: str
    email: str | None = None
    phone: str | None = None
    comments: str | None = None
    files: list[str] = []
    answers_file_url: str | None = None
    consent: bool
    marketing_consent: bool = False

    @field_validator("consent")
    @classmethod
    def validate_consent(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Необходимо согласие на обработку персональных данных")
        return value

    def to_entity(self) -> SubmissionEntity:
        return SubmissionEntity(
            form_type=FormTypeValueObject(value=self.form_type),
            name=NameValueObject(value=self.name),
            email=EmailValueObject(value=self.email) if self.email else None,
            phone=PhoneValueObject(value=self.phone) if self.phone else None,
            comments=CommentsValueObject(value=self.comments) if self.comments else None,
            files=self.files,
            answers_file_url=self.answers_file_url,
            consent=self.consent,
            marketing_consent=self.marketing_consent,
        )


class SubmissionCreatedEventSchema(BaseModel):
    submission_id: str
    form_type: str
    name: str
    email: str | None
    phone: str | None
    comments: str | None
    files: list[str]
    answers_file_url: str | None
    consent: bool
    marketing_consent: bool
    timestamp: str

    @classmethod
    def from_entity(cls, entity: SubmissionEntity) -> "SubmissionCreatedEventSchema":
        return cls(
            submission_id=str(entity.oid),
            form_type=entity.form_type.as_generic_type(),
            name=entity.name.as_generic_type(),
            email=entity.email.as_generic_type() if entity.email else None,
            phone=entity.phone.as_generic_type() if entity.phone else None,
            comments=entity.comments.as_generic_type() if entity.comments else None,
            files=entity.files,
            answers_file_url=entity.answers_file_url,
            consent=entity.consent,
            marketing_consent=entity.marketing_consent,
            timestamp=entity.created_at.strftime("%d.%m.%Y %H:%M"),
        )
