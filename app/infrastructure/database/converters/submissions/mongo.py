from datetime import datetime
from uuid import UUID

from domain.submissions.entities.submissions import SubmissionEntity
from domain.submissions.value_objects.submissions import (
    CommentsValueObject,
    EmailValueObject,
    FormTypeValueObject,
    NameValueObject,
    PhoneValueObject,
)


def submission_entity_to_document(entity: SubmissionEntity) -> dict:
    document = {
        "oid": str(entity.oid),
        "form_type": entity.form_type.as_generic_type(),
        "name": entity.name.as_generic_type(),
        "files": entity.files,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }

    if entity.email:
        document["email"] = entity.email.as_generic_type()
    if entity.phone:
        document["phone"] = entity.phone.as_generic_type()
    if entity.comments:
        document["comments"] = entity.comments.as_generic_type()
    if entity.answers_file_url is not None:
        document["answers_file_url"] = entity.answers_file_url

    return document


def submission_document_to_entity(document: dict) -> SubmissionEntity:
    return SubmissionEntity(
        oid=UUID(document["oid"]),
        form_type=FormTypeValueObject(value=document["form_type"]),
        name=NameValueObject(value=document["name"]),
        email=EmailValueObject(value=document.get("email")),
        phone=PhoneValueObject(value=document.get("phone")),
        comments=CommentsValueObject(value=document.get("comments")),
        files=document.get("files", []),
        answers_file_url=document.get("answers_file_url"),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
