from uuid import uuid4

from domain.vacancies.entities import VacancyEntity
from domain.vacancies.value_objects import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


def test_vacancy_entity_creation():
    title = TitleValueObject("Инженер-конструктор")
    requirements = RequirementsValueObject(
        [
            "Высшее техническое образование",
            "Опыт работы с CAD системами",
            "Знание ГОСТ и СНиП",
        ],
    )
    experience = ExperienceValueObject(
        [
            "Опыт работы от 3 лет",
            "Работа с металлоконструкциями",
        ],
    )
    salary = SalaryValueObject(80000)
    category = CategoryValueObject("Производство")

    vacancy = VacancyEntity(
        title=title,
        requirements=requirements,
        experience=experience,
        salary=salary,
        category=category,
    )

    assert vacancy.title.as_generic_type() == "Инженер-конструктор"
    assert vacancy.requirements.as_generic_type() == [
        "Высшее техническое образование",
        "Опыт работы с CAD системами",
        "Знание ГОСТ и СНиП",
    ]
    assert vacancy.experience.as_generic_type() == [
        "Опыт работы от 3 лет",
        "Работа с металлоконструкциями",
    ]
    assert vacancy.salary.as_generic_type() == 80000
    assert vacancy.category.as_generic_type() == "Производство"
    assert vacancy.oid is not None
    assert vacancy.created_at is not None
    assert vacancy.updated_at is not None


def test_vacancy_entity_creation_with_minimal_data():
    title = TitleValueObject("Менеджер по продажам")
    requirements = RequirementsValueObject(["Опыт в продажах"])
    experience = ExperienceValueObject(["Опыт работы от 1 года"])
    salary = SalaryValueObject(50000)
    category = CategoryValueObject("Продажи и маркетинг")

    vacancy = VacancyEntity(
        title=title,
        requirements=requirements,
        experience=experience,
        salary=salary,
        category=category,
    )

    assert vacancy.title.as_generic_type() == "Менеджер по продажам"
    assert len(vacancy.requirements.as_generic_type()) == 1
    assert len(vacancy.experience.as_generic_type()) == 1
    assert vacancy.salary.as_generic_type() == 50000
    assert vacancy.category.as_generic_type() == "Продажи и маркетинг"


def test_vacancy_entity_equality():
    vacancy_id = uuid4()
    title = TitleValueObject("Инженер-конструктор")
    requirements = RequirementsValueObject(["Требование 1"])
    experience = ExperienceValueObject(["Опыт 1"])
    salary = SalaryValueObject(80000)
    category = CategoryValueObject("Производство")

    vacancy1 = VacancyEntity(
        oid=vacancy_id,
        title=title,
        requirements=requirements,
        experience=experience,
        salary=salary,
        category=category,
    )

    vacancy2 = VacancyEntity(
        oid=vacancy_id,
        title=title,
        requirements=requirements,
        experience=experience,
        salary=salary,
        category=category,
    )

    vacancy3 = VacancyEntity(
        oid=uuid4(),
        title=title,
        requirements=requirements,
        experience=experience,
        salary=salary,
        category=category,
    )

    assert vacancy1 == vacancy2
    assert vacancy1 != vacancy3
