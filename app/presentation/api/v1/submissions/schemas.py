from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.value_objects.submissions import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
    QuestionnaireTypeValueObject,
)


class SubmissionResponseSchema(BaseModel):
    oid: UUID
    form_type: str
    name: str
    email: str | None
    phone: str | None
    comments: str | None
    files: list[str]
    questionnaire_html: Any | None
    questionnaire_answers: Any | None
    questionnaire_type: str | None
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
            questionnaire_html=entity.questionnaire_html,
            questionnaire_answers=entity.questionnaire_answers,
            questionnaire_type=entity.questionnaire_type.as_generic_type() if entity.questionnaire_type else None,
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
    questionnaire_html: str | None = None
    questionnaire_answers: Any | None = None
    questionnaire_type: str | None = None

    def to_entity(self) -> SubmissionEntity:
        return SubmissionEntity(
            form_type=FormTypeValueObject(value=self.form_type),
            name=NameValueObject(value=self.name),
            email=EmailValueObject(value=self.email) if self.email else None,
            phone=PhoneValueObject(value=self.phone) if self.phone else None,
            comments=CommentsValueObject(value=self.comments) if self.comments else None,
            files=self.files,
            questionnaire_html=self.questionnaire_html,
            questionnaire_answers=self.questionnaire_answers,
            questionnaire_type=QuestionnaireTypeValueObject(value=self.questionnaire_type)
            if self.questionnaire_type
            else None,
        )


class SubmissionCreatedEventSchema(BaseModel):
    submission_id: str
    form_type: str
    name: str
    email: str | None
    phone: str | None
    comments: str | None
    files: list[str]
    questionnaire_html: Any | None
    questionnaire_answers: Any | None
    questionnaire_type: str | None
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
            questionnaire_html=entity.questionnaire_html,
            questionnaire_answers=entity.questionnaire_answers,
            questionnaire_type=entity.questionnaire_type.as_generic_type() if entity.questionnaire_type else None,
            timestamp=datetime.now().isoformat(),
        )
