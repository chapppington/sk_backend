import pytest
from faker import Faker


@pytest.fixture
def valid_product_data(faker: Faker) -> dict:
    return {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
        "important_characteristics": [],
        "advantages": [],
        "simple_description": [],
        "detailed_description": [],
        "documentation": None,
        "order": 0,
        "is_shown": True,
        "show_advantages": True,
        "portfolio_ids": [],
    }


@pytest.fixture
def valid_product_data_with_category(faker: Faker):
    def _create(category: str = "Трансформаторные подстанции") -> dict:
        return {
            "category": category,
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
            "important_characteristics": [],
            "advantages": [],
            "simple_description": [],
            "detailed_description": [],
            "documentation": None,
            "order": 0,
            "is_shown": True,
            "show_advantages": True,
            "portfolio_ids": [],
        }

    return _create
