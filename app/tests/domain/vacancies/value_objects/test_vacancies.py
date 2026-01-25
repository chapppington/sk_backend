import pytest

from domain.vacancies.exceptions import (
    CategoryInvalidException,
    ExperienceEmptyException,
    RequirementsEmptyException,
    SalaryInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)
from domain.vacancies.value_objects.vacancies import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


@pytest.mark.parametrize(
    "category_value,expected",
    [
        ("Кадровый резерв", "Кадровый резерв"),
        ("Производство", "Производство"),
        ("Продажи и маркетинг", "Продажи и маркетинг"),
        ("Офис компании", "Офис компании"),
    ],
)
def test_category_valid(category_value, expected):
    category = CategoryValueObject(category_value)
    assert category.as_generic_type() == expected


@pytest.mark.parametrize(
    "category_value,exception",
    [
        ("", CategoryInvalidException),
        ("invalid", CategoryInvalidException),
        ("engineering", CategoryInvalidException),
        ("Кадровый резер", CategoryInvalidException),
    ],
)
def test_category_invalid(category_value, exception):
    with pytest.raises(exception):
        CategoryValueObject(category_value)


@pytest.mark.parametrize(
    "title_value,expected",
    [
        ("Инженер-конструктор", "Инженер-конструктор"),
        ("A" * 255, "A" * 255),
        ("Менеджер по продажам", "Менеджер по продажам"),
    ],
)
def test_title_valid(title_value, expected):
    title = TitleValueObject(title_value)
    assert title.as_generic_type() == expected


@pytest.mark.parametrize(
    "title_value,exception",
    [
        ("", TitleEmptyException),
        ("A" * 256, TitleTooLongException),
    ],
)
def test_title_invalid(title_value, exception):
    with pytest.raises(exception):
        TitleValueObject(title_value)


@pytest.mark.parametrize(
    "requirements_value,expected",
    [
        (["Высшее техническое образование"], ["Высшее техническое образование"]),
        (
            ["Требование 1", "Требование 2", "Требование 3"],
            ["Требование 1", "Требование 2", "Требование 3"],
        ),
        (["Опыт работы от 3 лет"], ["Опыт работы от 3 лет"]),
    ],
)
def test_requirements_valid(requirements_value, expected):
    requirements = RequirementsValueObject(requirements_value)
    assert requirements.as_generic_type() == expected


@pytest.mark.parametrize(
    "requirements_value,exception",
    [
        ([], RequirementsEmptyException),
    ],
)
def test_requirements_invalid(requirements_value, exception):
    with pytest.raises(exception):
        RequirementsValueObject(requirements_value)


@pytest.mark.parametrize(
    "experience_value,expected",
    [
        (["Опыт работы от 3 лет"], ["Опыт работы от 3 лет"]),
        (
            ["Опыт работы от 3 лет", "Работа с металлоконструкциями"],
            ["Опыт работы от 3 лет", "Работа с металлоконструкциями"],
        ),
        (["Опыт в продажах"], ["Опыт в продажах"]),
    ],
)
def test_experience_valid(experience_value, expected):
    experience = ExperienceValueObject(experience_value)
    assert experience.as_generic_type() == expected


@pytest.mark.parametrize(
    "experience_value,exception",
    [
        ([], ExperienceEmptyException),
    ],
)
def test_experience_invalid(experience_value, exception):
    with pytest.raises(exception):
        ExperienceValueObject(experience_value)


@pytest.mark.parametrize(
    "salary_value,expected",
    [
        (0, 0),
        (50000, 50000),
        (80000, 80000),
        (150000, 150000),
    ],
)
def test_salary_valid(salary_value, expected):
    salary = SalaryValueObject(salary_value)
    assert salary.as_generic_type() == expected


@pytest.mark.parametrize(
    "salary_value,exception",
    [
        (-1, SalaryInvalidException),
        (-100, SalaryInvalidException),
        (-1000, SalaryInvalidException),
    ],
)
def test_salary_invalid(salary_value, exception):
    with pytest.raises(exception):
        SalaryValueObject(salary_value)
