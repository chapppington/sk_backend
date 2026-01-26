from domain.products.entities.advantages import AdvantageEntity
from domain.products.entities.detailed_descriptions import DetailedDescriptionEntity
from domain.products.entities.documentations import DocumentationEntity
from domain.products.entities.important_characteristics import (
    ImportantCharacteristicEntity,
    ImportantCharacteristicUnit,
)
from domain.products.entities.products import ProductEntity
from domain.products.entities.simple_descriptions import SimpleDescriptionEntity


__all__ = [
    "ProductEntity",
    "ImportantCharacteristicEntity",
    "ImportantCharacteristicUnit",
    "AdvantageEntity",
    "SimpleDescriptionEntity",
    "DetailedDescriptionEntity",
    "DocumentationEntity",
]
