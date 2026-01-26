from datetime import datetime
from uuid import UUID

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


def seo_settings_entity_to_document(entity: SeoSettingsEntity) -> dict:
    document = {
        "oid": str(entity.oid),
        "page_path": entity.page_path.as_generic_type(),
        "page_name": entity.page_name.as_generic_type(),
        "title": entity.title.as_generic_type(),
        "description": entity.description.as_generic_type(),
        "is_active": entity.is_active,
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }

    if entity.keywords:
        document["keywords"] = entity.keywords.as_generic_type()
    if entity.og_title:
        document["og_title"] = entity.og_title.as_generic_type()
    if entity.og_description:
        document["og_description"] = entity.og_description.as_generic_type()
    if entity.og_image:
        document["og_image"] = entity.og_image.as_generic_type()
    if entity.canonical_url:
        document["canonical_url"] = entity.canonical_url.as_generic_type()

    return document


def seo_settings_document_to_entity(document: dict) -> SeoSettingsEntity:
    return SeoSettingsEntity(
        oid=UUID(document["oid"]),
        page_path=PagePathValueObject(value=document["page_path"]),
        page_name=PageNameValueObject(value=document["page_name"]),
        title=TitleValueObject(value=document["title"]),
        description=DescriptionValueObject(value=document["description"]),
        keywords=KeywordsValueObject(value=document.get("keywords")) if document.get("keywords") else None,
        og_title=OgTitleValueObject(value=document.get("og_title")) if document.get("og_title") else None,
        og_description=OgDescriptionValueObject(value=document.get("og_description"))
        if document.get("og_description")
        else None,
        og_image=OgImageValueObject(value=document.get("og_image")) if document.get("og_image") else None,
        canonical_url=CanonicalUrlValueObject(value=document.get("canonical_url"))
        if document.get("canonical_url")
        else None,
        is_active=document.get("is_active", True),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
