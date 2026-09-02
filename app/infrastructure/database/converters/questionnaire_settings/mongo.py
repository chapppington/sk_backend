from datetime import datetime
from uuid import UUID

from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.value_objects import (
    BreadcrumbLabelValueObject,
    H1ValueObject,
    PageNameValueObject,
    QuestionnaireSlugValueObject,
    SubtitleValueObject,
)


def questionnaire_settings_entity_to_document(entity: QuestionnaireSettingsEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "slug": entity.slug.as_generic_type(),
        "page_name": entity.page_name.as_generic_type(),
        "h1": entity.h1.as_generic_type(),
        "subtitle": entity.subtitle.as_generic_type(),
        "breadcrumb_label": entity.breadcrumb_label.as_generic_type(),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def questionnaire_settings_document_to_entity(document: dict) -> QuestionnaireSettingsEntity:
    return QuestionnaireSettingsEntity(
        oid=UUID(document["oid"]),
        slug=QuestionnaireSlugValueObject(value=document["slug"]),
        page_name=PageNameValueObject(value=document["page_name"]),
        h1=H1ValueObject(value=document["h1"]),
        subtitle=SubtitleValueObject(value=document["subtitle"]),
        breadcrumb_label=BreadcrumbLabelValueObject(value=document["breadcrumb_label"]),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
