from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.catalog_texts.value_objects import (
    CatalogCategoryValueObject,
    CatalogTextContentValueObject,
)


@dataclass(eq=False)
class CatalogTextEntity(BaseEntity):
    category: CatalogCategoryValueObject
    content: CatalogTextContentValueObject
