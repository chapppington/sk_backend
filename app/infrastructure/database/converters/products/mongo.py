from datetime import datetime
from uuid import UUID

from domain.products.entities import (
    AdvantageEntity,
    DetailedDescriptionEntity,
    DocumentationEntity,
    ImportantCharacteristicEntity,
    ImportantCharacteristicUnit,
    ProductEntity,
    SimpleDescriptionEntity,
)
from domain.products.value_objects import (
    CategoryValueObject,
    DescriptionValueObject,
    NameValueObject,
    PreviewImageAltValueObject,
    PreviewImageUrlValueObject,
    SlugValueObject,
)


def product_entity_to_document(entity: ProductEntity) -> dict:
    document = {
        "oid": str(entity.oid),
        "category": entity.category.as_generic_type(),
        "name": entity.name.as_generic_type(),
        "slug": entity.slug.as_generic_type(),
        "description": entity.description.as_generic_type(),
        "preview_image_url": entity.preview_image_url.as_generic_type(),
        "important_characteristics": [
            {
                "value": char.value,
                "unit": {"text": char.unit.text} if char.unit else None,
                "description": char.description,
            }
            for char in entity.important_characteristics
        ],
        "advantages": [
            {
                "label": adv.label,
                "icon": adv.icon,
                "image": adv.image,
                "alt": adv.alt,
                "description": adv.description,
            }
            for adv in entity.advantages
        ],
        "simple_description": [{"text": desc.text} for desc in entity.simple_description],
        "detailed_description": [
            {"title": desc.title, "description": desc.description} for desc in entity.detailed_description
        ],
        "order": entity.order,
        "is_shown": entity.is_shown,
        "show_advantages": entity.show_advantages,
        "portfolio_ids": [str(pid) for pid in entity.portfolio_ids],
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }

    if entity.preview_image_alt:
        document["preview_image_alt"] = entity.preview_image_alt.as_generic_type()
    if entity.documentation:
        document["documentation"] = [
            {"title": doc.title, "url": doc.url, "type": doc.type} for doc in entity.documentation
        ]

    return document


def product_document_to_entity(document: dict) -> ProductEntity:
    important_characteristics = []
    for char_data in document.get("important_characteristics", []):
        unit = None
        if char_data.get("unit"):
            unit = ImportantCharacteristicUnit(text=char_data["unit"]["text"])
        important_characteristics.append(
            ImportantCharacteristicEntity(
                value=char_data["value"],
                unit=unit,
                description=char_data.get("description", ""),
            ),
        )

    advantages = []
    for adv_data in document.get("advantages", []):
        advantages.append(
            AdvantageEntity(
                label=adv_data["label"],
                icon=adv_data["icon"],
                image=adv_data.get("image"),
                alt=adv_data.get("alt"),
                description=adv_data.get("description", ""),
            ),
        )

    simple_description = [
        SimpleDescriptionEntity(text=desc_data["text"]) for desc_data in document.get("simple_description", [])
    ]

    detailed_description = [
        DetailedDescriptionEntity(title=desc_data["title"], description=desc_data["description"])
        for desc_data in document.get("detailed_description", [])
    ]

    documentation = None
    if document.get("documentation"):
        documentation = [
            DocumentationEntity(
                title=doc_data["title"],
                url=doc_data["url"],
                type=doc_data["type"],
            )
            for doc_data in document["documentation"]
        ]

    portfolio_ids = [UUID(pid) for pid in document.get("portfolio_ids", [])]

    return ProductEntity(
        oid=UUID(document["oid"]),
        category=CategoryValueObject(value=document["category"]),
        name=NameValueObject(value=document["name"]),
        slug=SlugValueObject(value=document["slug"]),
        description=DescriptionValueObject(value=document["description"]),
        preview_image_url=PreviewImageUrlValueObject(value=document["preview_image_url"]),
        preview_image_alt=PreviewImageAltValueObject(value=document.get("preview_image_alt")),
        important_characteristics=important_characteristics,
        advantages=advantages,
        simple_description=simple_description,
        detailed_description=detailed_description,
        documentation=documentation,
        order=document.get("order", 0),
        is_shown=document.get("is_shown", True),
        show_advantages=document.get("show_advantages", True),
        portfolio_ids=portfolio_ids,
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
