import pytest
from faker import Faker


@pytest.fixture
def valid_vacancy_data(faker: Faker) -> dict:
    return {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
            faker.sentence(nb_words=6),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }


@pytest.fixture
def valid_vacancy_data_with_category(faker: Faker):
    def _create(category: str = "Производство") -> dict:
        return {
            "title": faker.job(),
            "requirements": [
                faker.sentence(nb_words=5),
                faker.sentence(nb_words=6),
            ],
            "experience": [
                faker.sentence(nb_words=4),
            ],
            "salary": faker.random_int(min=30000, max=200000),
            "category": category,
        }

    return _create
