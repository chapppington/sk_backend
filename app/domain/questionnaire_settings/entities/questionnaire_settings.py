from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.questionnaire_settings.value_objects import (
    BreadcrumbLabelValueObject,
    H1ValueObject,
    PageNameValueObject,
    QuestionnaireSlugValueObject,
    SubtitleValueObject,
)


@dataclass(eq=False)
class QuestionnaireSettingsEntity(BaseEntity):
    slug: QuestionnaireSlugValueObject
    page_name: PageNameValueObject
    h1: H1ValueObject
    subtitle: SubtitleValueObject
    breadcrumb_label: BreadcrumbLabelValueObject
