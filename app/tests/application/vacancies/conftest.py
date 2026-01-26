import pytest
from faker import Faker

from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.value_objects.vacancies import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


@pytest.fixture
def valid_vacancy_entity(faker: Faker) -> VacancyEntity:
    return VacancyEntity(
        title=TitleValueObject(value=faker.job()),
        requirements=RequirementsValueObject(
            value=[
                faker.sentence(nb_words=5),
                faker.sentence(nb_words=6),
            ],
        ),
        experience=ExperienceValueObject(value=[faker.sentence(nb_words=4)]),
        salary=SalaryValueObject(value=faker.random_int(min=30000, max=200000)),
        category=CategoryValueObject(value="Производство"),
    )


@pytest.fixture
def valid_vacancy_entity_with_category(faker: Faker):
    def _create(category: str = "Производство") -> VacancyEntity:
        return VacancyEntity(
            title=TitleValueObject(value=faker.job()),
            requirements=RequirementsValueObject(
                value=[
                    faker.sentence(nb_words=5),
                    faker.sentence(nb_words=6),
                ],
            ),
            experience=ExperienceValueObject(value=[faker.sentence(nb_words=4)]),
            salary=SalaryValueObject(value=faker.random_int(min=30000, max=200000)),
            category=CategoryValueObject(value=category),
        )

    return _create
