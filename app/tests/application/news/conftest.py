from datetime import datetime

import pytest
from faker import Faker


@pytest.fixture
def valid_news_data(faker: Faker) -> dict:
    return {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }


@pytest.fixture
def valid_news_data_with_category(faker: Faker):
    def _create(category: str = "События") -> dict:
        return {
            "category": category,
            "title": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "content": faker.text(max_nb_chars=1000),
            "short_content": faker.text(max_nb_chars=200),
            "image_url": faker.image_url(),
            "alt": faker.sentence(nb_words=3),
            "reading_time": faker.random_int(min=1, max=60),
            "date": datetime.now(),
        }

    return _create
