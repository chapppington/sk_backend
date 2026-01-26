from datetime import datetime

import pytest
from faker import Faker

from domain.news.entities.news import NewsEntity
from domain.news.value_objects.news import (
    AltValueObject,
    CategoryValueObject,
    ContentValueObject,
    ImageUrlValueObject,
    ReadingTimeValueObject,
    ShortContentValueObject,
    SlugValueObject,
    TitleValueObject,
)


@pytest.fixture
def valid_news_entity(faker: Faker) -> NewsEntity:
    return NewsEntity(
        category=CategoryValueObject(value="События"),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        slug=SlugValueObject(value=faker.slug()),
        content=ContentValueObject(value=faker.text(max_nb_chars=1000)),
        short_content=ShortContentValueObject(value=faker.text(max_nb_chars=200)),
        image_url=ImageUrlValueObject(value=faker.image_url()),
        alt=AltValueObject(value=faker.sentence(nb_words=3)),
        reading_time=ReadingTimeValueObject(value=faker.random_int(min=1, max=60)),
        date=datetime.now(),
    )


@pytest.fixture
def valid_news_entity_with_category(faker: Faker):
    def _create(category: str = "События") -> NewsEntity:
        return NewsEntity(
            category=CategoryValueObject(value=category),
            title=TitleValueObject(value=faker.sentence(nb_words=5)),
            slug=SlugValueObject(value=faker.slug()),
            content=ContentValueObject(value=faker.text(max_nb_chars=1000)),
            short_content=ShortContentValueObject(value=faker.text(max_nb_chars=200)),
            image_url=ImageUrlValueObject(value=faker.image_url()),
            alt=AltValueObject(value=faker.sentence(nb_words=3)),
            reading_time=ReadingTimeValueObject(value=faker.random_int(min=1, max=60)),
            date=datetime.now(),
        )

    return _create
