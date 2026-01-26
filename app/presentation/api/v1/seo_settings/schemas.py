from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain.seo_settings.entities import SeoSettingsEntity
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


class SeoSettingsResponseSchema(BaseModel):
    oid: UUID
    page_path: str
    page_name: str
    title: str
    description: str
    keywords: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    canonical_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: SeoSettingsEntity) -> "SeoSettingsResponseSchema":
        return cls(
            oid=entity.oid,
            page_path=entity.page_path.as_generic_type(),
            page_name=entity.page_name.as_generic_type(),
            title=entity.title.as_generic_type(),
            description=entity.description.as_generic_type(),
            keywords=entity.keywords.as_generic_type() if entity.keywords else None,
            og_title=entity.og_title.as_generic_type() if entity.og_title else None,
            og_description=entity.og_description.as_generic_type() if entity.og_description else None,
            og_image=entity.og_image.as_generic_type() if entity.og_image else None,
            canonical_url=entity.canonical_url.as_generic_type() if entity.canonical_url else None,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class SeoSettingsRequestSchema(BaseModel):
    page_path: str
    page_name: str
    title: str
    description: str
    keywords: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    canonical_url: Optional[str] = None
    is_active: bool = True

    def to_entity(self) -> SeoSettingsEntity:
        return SeoSettingsEntity(
            page_path=PagePathValueObject(value=self.page_path),
            page_name=PageNameValueObject(value=self.page_name),
            title=TitleValueObject(value=self.title),
            description=DescriptionValueObject(value=self.description),
            keywords=KeywordsValueObject(value=self.keywords) if self.keywords else None,
            og_title=OgTitleValueObject(value=self.og_title) if self.og_title else None,
            og_description=OgDescriptionValueObject(value=self.og_description) if self.og_description else None,
            og_image=OgImageValueObject(value=self.og_image) if self.og_image else None,
            canonical_url=CanonicalUrlValueObject(value=self.canonical_url) if self.canonical_url else None,
            is_active=self.is_active,
        )
