import pytest

from domain.portfolios.exceptions import (
    DescriptionEmptyException,
    NameEmptyException,
    NameTooLongException,
    PosterUrlInvalidException,
    ReviewImageUrlInvalidException,
    SlugEmptyException,
    SlugInvalidException,
    SolutionDescriptionEmptyException,
    SolutionImageUrlInvalidException,
    SolutionSubdescriptionEmptyException,
    SolutionSubtitleEmptyException,
    SolutionTitleEmptyException,
    TaskDescriptionEmptyException,
    TaskTitleEmptyException,
    VideoUrlInvalidException,
    YearInvalidException,
)
from domain.portfolios.value_objects.portfolios import (
    DescriptionValueObject,
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
    VideoUrlValueObject,
    YearValueObject,
)


@pytest.mark.parametrize(
    "name_value,expected",
    [
        ("Проект автоматизации склада", "Проект автоматизации склада"),
        ("A" * 255, "A" * 255),
        ("Тестовый проект", "Тестовый проект"),
    ],
)
def test_name_valid(name_value, expected):
    name = NameValueObject(name_value)
    assert name.as_generic_type() == expected


@pytest.mark.parametrize(
    "name_value,exception",
    [
        ("", NameEmptyException),
        ("A" * 256, NameTooLongException),
    ],
)
def test_name_invalid(name_value, exception):
    with pytest.raises(exception):
        NameValueObject(name_value)


@pytest.mark.parametrize(
    "slug_value,expected",
    [
        ("proekt-avtomatizacii-sklada", "proekt-avtomatizacii-sklada"),
        ("test-slug", "test-slug"),
        ("slug123", "slug123"),
        ("test-slug-123", "test-slug-123"),
    ],
)
def test_slug_valid(slug_value, expected):
    slug = SlugValueObject(slug_value)
    assert slug.as_generic_type() == expected


@pytest.mark.parametrize(
    "slug_value,exception",
    [
        ("", SlugEmptyException),
        ("Invalid-Slug", SlugInvalidException),
        ("invalid slug", SlugInvalidException),
        ("invalid_slug", SlugInvalidException),
        ("-invalid", SlugInvalidException),
        ("invalid-", SlugInvalidException),
        ("A" * 256, SlugInvalidException),
    ],
)
def test_slug_invalid(slug_value, exception):
    with pytest.raises(exception):
        SlugValueObject(slug_value)


@pytest.mark.parametrize(
    "poster_url_value,expected",
    [
        (
            "https://sibkomplekt.ru/images/portfolio/warehouse-poster.jpg",
            "https://sibkomplekt.ru/images/portfolio/warehouse-poster.jpg",
        ),
        ("http://example.com/poster.png", "http://example.com/poster.png"),
    ],
)
def test_poster_url_valid(poster_url_value, expected):
    poster_url = PosterUrlValueObject(poster_url_value)
    assert poster_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "poster_url_value,exception",
    [
        ("", PosterUrlInvalidException),
        ("not-a-url", PosterUrlInvalidException),
        ("ftp://example.com/poster.jpg", PosterUrlInvalidException),
    ],
)
def test_poster_url_invalid(poster_url_value, exception):
    with pytest.raises(exception):
        PosterUrlValueObject(poster_url_value)


@pytest.mark.parametrize(
    "year_value,expected",
    [
        (2000, 2000),
        (2025, 2025),
        (2100, 2100),
    ],
)
def test_year_valid(year_value, expected):
    year = YearValueObject(year_value)
    assert year.as_generic_type() == expected


@pytest.mark.parametrize(
    "year_value,exception",
    [
        (1999, YearInvalidException),
        (2101, YearInvalidException),
        (1500, YearInvalidException),
    ],
)
def test_year_invalid(year_value, exception):
    with pytest.raises(exception):
        YearValueObject(year_value)


@pytest.mark.parametrize(
    "task_title_value,expected",
    [
        ("Задача проекта", "Задача проекта"),
        ("Тестовая задача", "Тестовая задача"),
    ],
)
def test_task_title_valid(task_title_value, expected):
    task_title = TaskTitleValueObject(task_title_value)
    assert task_title.as_generic_type() == expected


@pytest.mark.parametrize(
    "task_title_value,exception",
    [
        ("", TaskTitleEmptyException),
    ],
)
def test_task_title_invalid(task_title_value, exception):
    with pytest.raises(exception):
        TaskTitleValueObject(task_title_value)


@pytest.mark.parametrize(
    "task_description_value,expected",
    [
        ("Автоматизировать процессы управления складом", "Автоматизировать процессы управления складом"),
        ("Описание задачи", "Описание задачи"),
    ],
)
def test_task_description_valid(task_description_value, expected):
    task_description = TaskDescriptionValueObject(task_description_value)
    assert task_description.as_generic_type() == expected


@pytest.mark.parametrize(
    "task_description_value,exception",
    [
        ("", TaskDescriptionEmptyException),
    ],
)
def test_task_description_invalid(task_description_value, exception):
    with pytest.raises(exception):
        TaskDescriptionValueObject(task_description_value)


@pytest.mark.parametrize(
    "solution_title_value,expected",
    [
        ("Решение", "Решение"),
        ("Тестовое решение", "Тестовое решение"),
    ],
)
def test_solution_title_valid(solution_title_value, expected):
    solution_title = SolutionTitleValueObject(solution_title_value)
    assert solution_title.as_generic_type() == expected


@pytest.mark.parametrize(
    "solution_title_value,exception",
    [
        ("", SolutionTitleEmptyException),
    ],
)
def test_solution_title_invalid(solution_title_value, exception):
    with pytest.raises(exception):
        SolutionTitleValueObject(solution_title_value)


@pytest.mark.parametrize(
    "solution_description_value,expected",
    [
        ("Разработана комплексная система управления складом", "Разработана комплексная система управления складом"),
        ("Описание решения", "Описание решения"),
    ],
)
def test_solution_description_valid(solution_description_value, expected):
    solution_description = SolutionDescriptionValueObject(solution_description_value)
    assert solution_description.as_generic_type() == expected


@pytest.mark.parametrize(
    "solution_description_value,exception",
    [
        ("", SolutionDescriptionEmptyException),
    ],
)
def test_solution_description_invalid(solution_description_value, exception):
    with pytest.raises(exception):
        SolutionDescriptionValueObject(solution_description_value)


@pytest.mark.parametrize(
    "solution_subtitle_value,expected",
    [
        ("Результаты", "Результаты"),
        ("Тестовый подзаголовок", "Тестовый подзаголовок"),
    ],
)
def test_solution_subtitle_valid(solution_subtitle_value, expected):
    solution_subtitle = SolutionSubtitleValueObject(solution_subtitle_value)
    assert solution_subtitle.as_generic_type() == expected


@pytest.mark.parametrize(
    "solution_subtitle_value,exception",
    [
        ("", SolutionSubtitleEmptyException),
    ],
)
def test_solution_subtitle_invalid(solution_subtitle_value, exception):
    with pytest.raises(exception):
        SolutionSubtitleValueObject(solution_subtitle_value)


@pytest.mark.parametrize(
    "solution_subdescription_value,expected",
    [
        ("Сокращение времени обработки заказов на 40%", "Сокращение времени обработки заказов на 40%"),
        ("Описание результатов", "Описание результатов"),
    ],
)
def test_solution_subdescription_valid(solution_subdescription_value, expected):
    solution_subdescription = SolutionSubdescriptionValueObject(solution_subdescription_value)
    assert solution_subdescription.as_generic_type() == expected


@pytest.mark.parametrize(
    "solution_subdescription_value,exception",
    [
        ("", SolutionSubdescriptionEmptyException),
    ],
)
def test_solution_subdescription_invalid(solution_subdescription_value, exception):
    with pytest.raises(exception):
        SolutionSubdescriptionValueObject(solution_subdescription_value)


@pytest.mark.parametrize(
    "solution_image_url_value,expected",
    [
        (
            "https://sibkomplekt.ru/images/portfolio/solution-left.jpg",
            "https://sibkomplekt.ru/images/portfolio/solution-left.jpg",
        ),
        ("http://example.com/image.png", "http://example.com/image.png"),
    ],
)
def test_solution_image_url_valid(solution_image_url_value, expected):
    solution_image_url = SolutionImageUrlValueObject(solution_image_url_value)
    assert solution_image_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "solution_image_url_value,exception",
    [
        ("", SolutionImageUrlInvalidException),
        ("not-a-url", SolutionImageUrlInvalidException),
        ("ftp://example.com/image.jpg", SolutionImageUrlInvalidException),
    ],
)
def test_solution_image_url_invalid(solution_image_url_value, exception):
    with pytest.raises(exception):
        SolutionImageUrlValueObject(solution_image_url_value)


@pytest.mark.parametrize(
    "video_url_value,expected",
    [
        (
            "https://sibkomplekt.ru/videos/portfolio/preview-warehouse.mp4",
            "https://sibkomplekt.ru/videos/portfolio/preview-warehouse.mp4",
        ),
        ("http://example.com/video.mp4", "http://example.com/video.mp4"),
    ],
)
def test_video_url_valid(video_url_value, expected):
    video_url = VideoUrlValueObject(video_url_value)
    assert video_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "video_url_value,exception",
    [
        ("", VideoUrlInvalidException),
        ("not-a-url", VideoUrlInvalidException),
        ("ftp://example.com/video.mp4", VideoUrlInvalidException),
    ],
)
def test_video_url_invalid(video_url_value, exception):
    with pytest.raises(exception):
        VideoUrlValueObject(video_url_value)


@pytest.mark.parametrize(
    "description_value,expected",
    [
        ("Полное описание проекта портфолио", "Полное описание проекта портфолио"),
        ("Описание проекта", "Описание проекта"),
    ],
)
def test_description_valid(description_value, expected):
    description = DescriptionValueObject(description_value)
    assert description.as_generic_type() == expected


@pytest.mark.parametrize(
    "description_value,exception",
    [
        ("", DescriptionEmptyException),
    ],
)
def test_description_invalid(description_value, exception):
    with pytest.raises(exception):
        DescriptionValueObject(description_value)


@pytest.mark.parametrize(
    "review_title_value,expected",
    [
        ("Отличная работа!", "Отличная работа!"),
        (None, None),
        ("", None),
    ],
)
def test_review_title_valid(review_title_value, expected):
    review_title = ReviewTitleValueObject(review_title_value)
    assert review_title.as_generic_type() == expected


@pytest.mark.parametrize(
    "review_text_value,expected",
    [
        ("Команда выполнила проект в срок", "Команда выполнила проект в срок"),
        (None, None),
        ("", None),
    ],
)
def test_review_text_valid(review_text_value, expected):
    review_text = ReviewTextValueObject(review_text_value)
    assert review_text.as_generic_type() == expected


@pytest.mark.parametrize(
    "review_name_value,expected",
    [
        ("Иван Петров", "Иван Петров"),
        (None, None),
        ("", None),
    ],
)
def test_review_name_valid(review_name_value, expected):
    review_name = ReviewNameValueObject(review_name_value)
    assert review_name.as_generic_type() == expected


@pytest.mark.parametrize(
    "review_image_url_value,expected",
    [
        (
            "https://sibkomplekt.ru/images/reviews/ivan-petrov.jpg",
            "https://sibkomplekt.ru/images/reviews/ivan-petrov.jpg",
        ),
        (None, None),
        ("http://example.com/review.jpg", "http://example.com/review.jpg"),
    ],
)
def test_review_image_url_valid(review_image_url_value, expected):
    review_image_url = ReviewImageUrlValueObject(review_image_url_value)
    assert review_image_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "review_image_url_value,exception",
    [
        ("not-a-url", ReviewImageUrlInvalidException),
        ("ftp://example.com/review.jpg", ReviewImageUrlInvalidException),
    ],
)
def test_review_image_url_invalid(review_image_url_value, exception):
    with pytest.raises(exception):
        ReviewImageUrlValueObject(review_image_url_value)


@pytest.mark.parametrize(
    "review_role_value,expected",
    [
        ("Директор по логистике", "Директор по логистике"),
        (None, None),
        ("", None),
    ],
)
def test_review_role_valid(review_role_value, expected):
    review_role = ReviewRoleValueObject(review_role_value)
    assert review_role.as_generic_type() == expected
