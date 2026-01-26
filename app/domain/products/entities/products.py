from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.base.entity import BaseEntity
from domain.products.entities.advantages import AdvantageEntity
from domain.products.entities.detailed_descriptions import DetailedDescriptionEntity
from domain.products.entities.documentations import DocumentationEntity
from domain.products.entities.important_characteristics import ImportantCharacteristicEntity
from domain.products.entities.simple_descriptions import SimpleDescriptionEntity
from domain.products.value_objects import (
    CategoryValueObject,
    DescriptionValueObject,
    NameValueObject,
    PreviewImageAltValueObject,
    PreviewImageUrlValueObject,
    SlugValueObject,
)


@dataclass(eq=False)
class ProductEntity(BaseEntity):
    category: CategoryValueObject
    name: NameValueObject
    slug: SlugValueObject
    description: DescriptionValueObject
    preview_image_url: PreviewImageUrlValueObject
    preview_image_alt: PreviewImageAltValueObject | None = None
    important_characteristics: list[ImportantCharacteristicEntity] = field(default_factory=list)
    advantages: list[AdvantageEntity] = field(default_factory=list)
    simple_description: list[SimpleDescriptionEntity] = field(default_factory=list)
    detailed_description: list[DetailedDescriptionEntity] = field(default_factory=list)
    documentation: list[DocumentationEntity] | None = None
    order: int = 0
    is_shown: bool = True
    show_advantages: bool = True
    portfolio_ids: list[UUID] = field(default_factory=list)
