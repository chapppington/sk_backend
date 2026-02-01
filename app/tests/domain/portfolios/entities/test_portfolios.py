from domain.portfolios.entities import PortfolioEntity
from domain.portfolios.value_objects import (
    DescriptionValueObject,
    ImageAltValueObject,
    NameValueObject,
    PosterUrlValueObject,
    ReviewImageUrlValueObject,
    ReviewNameValueObject,
    ReviewRoleValueObject,
    ReviewTextValueObject,
    ReviewTitleValueObject,
    SlugValueObject,
    SolutionDescriptionValueObject,
    SolutionImageUrlValueObject,
    SolutionSubdescriptionValueObject,
    SolutionSubtitleValueObject,
    SolutionTitleValueObject,
    TaskDescriptionValueObject,
    TaskTitleValueObject,
    YearValueObject,
)


def test_portfolio_entity_creation():
    name = NameValueObject("Проект автоматизации склада")
    slug = SlugValueObject("proekt-avtomatizacii-sklada")
    poster = PosterUrlValueObject("https://sibkomplekt.ru/images/portfolio/warehouse-poster.jpg")
    poster_alt = ImageAltValueObject("Постер проекта автоматизации склада")
    year = YearValueObject(2025)
    description = DescriptionValueObject("Полное описание проекта портфолио с деталями реализации")
    task_title = TaskTitleValueObject("Задача проекта")
    task_description = TaskDescriptionValueObject("Автоматизировать процессы управления складом")
    solution_title = SolutionTitleValueObject("Решение")
    solution_description = SolutionDescriptionValueObject("Разработана комплексная система управления складом")
    solution_subtitle = SolutionSubtitleValueObject("Результаты")
    solution_subdescription = SolutionSubdescriptionValueObject("Сокращение времени обработки заказов на 40%")
    solution_image_left = SolutionImageUrlValueObject("https://sibkomplekt.ru/images/portfolio/solution-left.jpg")
    solution_image_left_alt = ImageAltValueObject("Схема решения слева")
    solution_image_right = SolutionImageUrlValueObject("https://sibkomplekt.ru/images/portfolio/solution-right.jpg")
    solution_image_right_alt = ImageAltValueObject("Схема решения справа")

    portfolio = PortfolioEntity(
        name=name,
        slug=slug,
        poster=poster,
        poster_alt=poster_alt,
        year=year,
        description=description,
        task_title=task_title,
        task_description=task_description,
        solution_title=solution_title,
        solution_description=solution_description,
        solution_subtitle=solution_subtitle,
        solution_subdescription=solution_subdescription,
        solution_image_left=solution_image_left,
        solution_image_left_alt=solution_image_left_alt,
        solution_image_right=solution_image_right,
        solution_image_right_alt=solution_image_right_alt,
        has_review=False,
    )

    assert portfolio.name.as_generic_type() == "Проект автоматизации склада"
    assert portfolio.slug.as_generic_type() == "proekt-avtomatizacii-sklada"
    assert portfolio.poster.as_generic_type() == "https://sibkomplekt.ru/images/portfolio/warehouse-poster.jpg"
    assert portfolio.year.as_generic_type() == 2025
    assert portfolio.task_title.as_generic_type() == "Задача проекта"
    assert portfolio.task_description.as_generic_type() == "Автоматизировать процессы управления складом"
    assert portfolio.solution_title.as_generic_type() == "Решение"
    assert portfolio.solution_description.as_generic_type() == "Разработана комплексная система управления складом"
    assert portfolio.solution_subtitle.as_generic_type() == "Результаты"
    assert portfolio.solution_subdescription.as_generic_type() == "Сокращение времени обработки заказов на 40%"
    assert (
        portfolio.solution_image_left.as_generic_type() == "https://sibkomplekt.ru/images/portfolio/solution-left.jpg"
    )
    assert (
        portfolio.solution_image_right.as_generic_type() == "https://sibkomplekt.ru/images/portfolio/solution-right.jpg"
    )
    assert portfolio.has_review is False
    assert portfolio.description.as_generic_type() == "Полное описание проекта портфолио с деталями реализации"
    assert portfolio.oid is not None
    assert portfolio.created_at is not None
    assert portfolio.updated_at is not None


def test_portfolio_entity_creation_with_review():
    name = NameValueObject("Проект автоматизации склада")
    slug = SlugValueObject("proekt-avtomatizacii-sklada")
    poster = PosterUrlValueObject("https://sibkomplekt.ru/images/portfolio/warehouse-poster.jpg")
    poster_alt = ImageAltValueObject("Постер проекта автоматизации склада")
    year = YearValueObject(2025)
    task_title = TaskTitleValueObject("Задача проекта")
    task_description = TaskDescriptionValueObject("Автоматизировать процессы управления складом")
    solution_title = SolutionTitleValueObject("Решение")
    solution_description = SolutionDescriptionValueObject("Разработана комплексная система управления складом")
    solution_subtitle = SolutionSubtitleValueObject("Результаты")
    solution_subdescription = SolutionSubdescriptionValueObject("Сокращение времени обработки заказов на 40%")
    solution_image_left = SolutionImageUrlValueObject("https://sibkomplekt.ru/images/portfolio/solution-left.jpg")
    solution_image_left_alt = ImageAltValueObject("Схема решения слева")
    solution_image_right = SolutionImageUrlValueObject("https://sibkomplekt.ru/images/portfolio/solution-right.jpg")
    solution_image_right_alt = ImageAltValueObject("Схема решения справа")
    description = DescriptionValueObject("Полное описание проекта портфолио с деталями реализации")
    review_title = ReviewTitleValueObject("Отличная работа!")
    review_text = ReviewTextValueObject("Команда выполнила проект в срок и с высоким качеством")
    review_name = ReviewNameValueObject("Иван Петров")
    review_image = ReviewImageUrlValueObject("https://sibkomplekt.ru/images/reviews/ivan-petrov.jpg")
    review_role = ReviewRoleValueObject("Директор по логистике")

    portfolio = PortfolioEntity(
        name=name,
        slug=slug,
        poster=poster,
        poster_alt=poster_alt,
        year=year,
        description=description,
        task_title=task_title,
        task_description=task_description,
        solution_title=solution_title,
        solution_description=solution_description,
        solution_subtitle=solution_subtitle,
        solution_subdescription=solution_subdescription,
        solution_image_left=solution_image_left,
        solution_image_left_alt=solution_image_left_alt,
        solution_image_right=solution_image_right,
        solution_image_right_alt=solution_image_right_alt,
        has_review=True,
        review_title=review_title,
        review_text=review_text,
        review_name=review_name,
        review_image=review_image,
        review_role=review_role,
    )

    assert portfolio.has_review is True
    assert portfolio.review_title.as_generic_type() == "Отличная работа!"
    assert portfolio.review_text.as_generic_type() == "Команда выполнила проект в срок и с высоким качеством"
    assert portfolio.review_name.as_generic_type() == "Иван Петров"
    assert portfolio.review_image.as_generic_type() == "https://sibkomplekt.ru/images/reviews/ivan-petrov.jpg"
    assert portfolio.review_role.as_generic_type() == "Директор по логистике"


def test_portfolio_entity_creation_with_optional_review_fields_none():
    name = NameValueObject("Проект автоматизации склада")
    slug = SlugValueObject("proekt-avtomatizacii-sklada")
    poster = PosterUrlValueObject("https://sibkomplekt.ru/images/portfolio/warehouse-poster.jpg")
    poster_alt = ImageAltValueObject("Постер проекта")
    year = YearValueObject(2025)
    description = DescriptionValueObject("Полное описание проекта портфолио с деталями реализации")
    task_title = TaskTitleValueObject("Задача проекта")
    task_description = TaskDescriptionValueObject("Автоматизировать процессы управления складом")
    solution_title = SolutionTitleValueObject("Решение")
    solution_description = SolutionDescriptionValueObject("Разработана комплексная система управления складом")
    solution_subtitle = SolutionSubtitleValueObject("Результаты")
    solution_subdescription = SolutionSubdescriptionValueObject("Сокращение времени обработки заказов на 40%")
    solution_image_left = SolutionImageUrlValueObject("https://sibkomplekt.ru/images/portfolio/solution-left.jpg")
    solution_image_left_alt = ImageAltValueObject("Схема слева")
    solution_image_right = SolutionImageUrlValueObject("https://sibkomplekt.ru/images/portfolio/solution-right.jpg")
    solution_image_right_alt = ImageAltValueObject("Схема справа")

    portfolio = PortfolioEntity(
        name=name,
        slug=slug,
        poster=poster,
        poster_alt=poster_alt,
        year=year,
        description=description,
        task_title=task_title,
        task_description=task_description,
        solution_title=solution_title,
        solution_description=solution_description,
        solution_subtitle=solution_subtitle,
        solution_subdescription=solution_subdescription,
        solution_image_left=solution_image_left,
        solution_image_left_alt=solution_image_left_alt,
        solution_image_right=solution_image_right,
        solution_image_right_alt=solution_image_right_alt,
        has_review=True,
        review_title=None,
        review_text=None,
        review_name=None,
        review_image=None,
        review_role=None,
    )

    assert portfolio.has_review is True
    assert portfolio.review_title is None
    assert portfolio.review_text is None
    assert portfolio.review_name is None
    assert portfolio.review_image is None
    assert portfolio.review_role is None
