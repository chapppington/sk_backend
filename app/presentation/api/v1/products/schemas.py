from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

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


class ImportantCharacteristicUnitSchema(BaseModel):
    text: str


class ImportantCharacteristicSchema(BaseModel):
    value: str
    unit: Optional[ImportantCharacteristicUnitSchema] = None
    description: str = ""


class AdvantageSchema(BaseModel):
    label: str
    icon: str
    image: Optional[str] = None
    alt: Optional[str] = None
    description: str = ""


class SimpleDescriptionSchema(BaseModel):
    text: str


class DetailedDescriptionSchema(BaseModel):
    title: str
    description: str


class DocumentationSchema(BaseModel):
    title: str
    url: str
    type: str


class ProductResponseSchema(BaseModel):
    oid: UUID
    category: str
    name: str
    slug: str
    description: str
    preview_image_url: str
    preview_image_alt: Optional[str] = None
    important_characteristics: list[ImportantCharacteristicSchema]
    advantages: list[AdvantageSchema]
    simple_description: list[SimpleDescriptionSchema]
    detailed_description: list[DetailedDescriptionSchema]
    documentation: Optional[list[DocumentationSchema]] = None
    order: int
    is_shown: bool
    show_advantages: bool
    portfolio_ids: list[UUID]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: ProductEntity) -> "ProductResponseSchema":
        return cls(
            oid=entity.oid,
            category=entity.category.as_generic_type(),
            name=entity.name.as_generic_type(),
            slug=entity.slug.as_generic_type(),
            description=entity.description.as_generic_type(),
            preview_image_url=entity.preview_image_url.as_generic_type(),
            preview_image_alt=entity.preview_image_alt.as_generic_type() if entity.preview_image_alt else None,
            important_characteristics=[
                ImportantCharacteristicSchema(
                    value=char.value,
                    unit=ImportantCharacteristicUnitSchema(text=char.unit.text) if char.unit else None,
                    description=char.description,
                )
                for char in entity.important_characteristics
            ],
            advantages=[
                AdvantageSchema(
                    label=adv.label,
                    icon=adv.icon,
                    image=adv.image,
                    alt=adv.alt,
                    description=adv.description,
                )
                for adv in entity.advantages
            ],
            simple_description=[SimpleDescriptionSchema(text=desc.text) for desc in entity.simple_description],
            detailed_description=[
                DetailedDescriptionSchema(title=desc.title, description=desc.description)
                for desc in entity.detailed_description
            ],
            documentation=[
                DocumentationSchema(title=doc.title, url=doc.url, type=doc.type) for doc in entity.documentation
            ]
            if entity.documentation
            else None,
            order=entity.order,
            is_shown=entity.is_shown,
            show_advantages=entity.show_advantages,
            portfolio_ids=entity.portfolio_ids,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class ProductOrderPatchSchema(BaseModel):
    order: int


class ProductRequestSchema(BaseModel):
    category: str
    name: str
    slug: str
    description: str
    preview_image_url: str
    preview_image_alt: Optional[str] = None
    important_characteristics: list[ImportantCharacteristicSchema] = []
    advantages: list[AdvantageSchema] = []
    simple_description: list[SimpleDescriptionSchema] = []
    detailed_description: list[DetailedDescriptionSchema] = []
    documentation: Optional[list[DocumentationSchema]] = None
    order: int = 0
    is_shown: bool = True
    show_advantages: bool = True
    portfolio_ids: list[UUID] = []

    def to_entity(self) -> ProductEntity:
        important_characteristics = [
            ImportantCharacteristicEntity(
                value=char.value,
                unit=ImportantCharacteristicUnit(text=char.unit.text) if char.unit else None,
                description=char.description,
            )
            for char in self.important_characteristics
        ]

        advantages = [
            AdvantageEntity(
                label=adv.label,
                icon=adv.icon,
                image=adv.image,
                alt=adv.alt,
                description=adv.description,
            )
            for adv in self.advantages
        ]

        simple_description = [SimpleDescriptionEntity(text=desc.text) for desc in self.simple_description]

        detailed_description = [
            DetailedDescriptionEntity(title=desc.title, description=desc.description)
            for desc in self.detailed_description
        ]

        documentation = None
        if self.documentation:
            documentation = [
                DocumentationEntity(
                    title=doc.title,
                    url=doc.url,
                    type=doc.type,
                )
                for doc in self.documentation
            ]

        return ProductEntity(
            category=CategoryValueObject(value=self.category),
            name=NameValueObject(value=self.name),
            slug=SlugValueObject(value=self.slug),
            description=DescriptionValueObject(value=self.description),
            preview_image_url=PreviewImageUrlValueObject(value=self.preview_image_url),
            preview_image_alt=PreviewImageAltValueObject(value=self.preview_image_alt),
            important_characteristics=important_characteristics,
            advantages=advantages,
            simple_description=simple_description,
            detailed_description=detailed_description,
            documentation=documentation,
            order=self.order,
            is_shown=self.is_shown,
            show_advantages=self.show_advantages,
            portfolio_ids=self.portfolio_ids,
        )
