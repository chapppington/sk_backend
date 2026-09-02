from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity
from domain.questionnaire_settings.value_objects import (
    BreadcrumbLabelValueObject,
    H1ValueObject,
    PageNameValueObject,
    QuestionnaireSlugValueObject,
    SubtitleValueObject,
)


class QuestionnaireSettingsResponseSchema(BaseModel):
    oid: UUID
    slug: str
    page_name: str
    h1: str
    subtitle: str
    breadcrumb_label: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: QuestionnaireSettingsEntity) -> "QuestionnaireSettingsResponseSchema":
        return cls(
            oid=entity.oid,
            slug=entity.slug.as_generic_type(),
            page_name=entity.page_name.as_generic_type(),
            h1=entity.h1.as_generic_type(),
            subtitle=entity.subtitle.as_generic_type(),
            breadcrumb_label=entity.breadcrumb_label.as_generic_type(),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class QuestionnaireSettingsRequestSchema(BaseModel):
    slug: str
    page_name: str
    h1: str
    subtitle: str
    breadcrumb_label: str

    def to_entity(self) -> QuestionnaireSettingsEntity:
        return QuestionnaireSettingsEntity(
            slug=QuestionnaireSlugValueObject(value=self.slug),
            page_name=PageNameValueObject(value=self.page_name),
            h1=H1ValueObject(value=self.h1),
            subtitle=SubtitleValueObject(value=self.subtitle),
            breadcrumb_label=BreadcrumbLabelValueObject(value=self.breadcrumb_label),
        )
