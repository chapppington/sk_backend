from dataclasses import dataclass
from typing import Optional

from domain.base.entity import BaseEntity
from domain.seo_settings.value_objects import (
    CanonicalUrlValueObject,
    DescriptionValueObject,
    KeywordsValueObject,
    OgDescriptionValueObject,
    OgImageValueObject,
    OgTitleValueObject,
    PageNameValueObject,
    PagePathValueObject,
    TitleValueObject,
)


@dataclass(eq=False)
class SeoSettingsEntity(BaseEntity):
    page_path: PagePathValueObject
    page_name: PageNameValueObject
    title: TitleValueObject
    description: DescriptionValueObject
    keywords: Optional[KeywordsValueObject] = None
    og_title: Optional[OgTitleValueObject] = None
    og_description: Optional[OgDescriptionValueObject] = None
    og_image: Optional[OgImageValueObject] = None
    canonical_url: Optional[CanonicalUrlValueObject] = None
    is_active: bool = True
