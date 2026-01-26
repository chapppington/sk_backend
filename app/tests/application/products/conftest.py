import pytest
from faker import Faker

from domain.products.entities import ProductEntity
from domain.products.value_objects import (
    CategoryValueObject,
    DescriptionValueObject,
    NameValueObject,
    PreviewImageAltValueObject,
    PreviewImageUrlValueObject,
    SlugValueObject,
)


@pytest.fixture
def valid_product_entity(faker: Faker) -> ProductEntity:
    return ProductEntity(
        category=CategoryValueObject(value="Трансформаторные подстанции"),
        name=NameValueObject(value=faker.sentence(nb_words=5)),
        slug=SlugValueObject(value=faker.slug()),
        description=DescriptionValueObject(value=faker.text(max_nb_chars=500)),
        preview_image_url=PreviewImageUrlValueObject(value=faker.image_url()),
        preview_image_alt=PreviewImageAltValueObject(value=faker.sentence(nb_words=3)),
    )


@pytest.fixture
def valid_product_entity_with_category(faker: Faker):
    def _create(category: str = "Трансформаторные подстанции") -> ProductEntity:
        return ProductEntity(
            category=CategoryValueObject(value=category),
            name=NameValueObject(value=faker.sentence(nb_words=5)),
            slug=SlugValueObject(value=faker.slug()),
            description=DescriptionValueObject(value=faker.text(max_nb_chars=500)),
            preview_image_url=PreviewImageUrlValueObject(value=faker.image_url()),
            preview_image_alt=PreviewImageAltValueObject(value=faker.sentence(nb_words=3)),
        )

    return _create
