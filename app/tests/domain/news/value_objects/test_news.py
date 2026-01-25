import pytest

from domain.news.exceptions import (
    AltTooLongException,
    CategoryInvalidException,
    ContentEmptyException,
    ReadingTimeInvalidException,
    ShortContentEmptyException,
    ShortContentTooLongException,
    SlugEmptyException,
    SlugInvalidException,
    TitleEmptyException,
    TitleTooLongException,
)
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


@pytest.mark.parametrize(
    "category_value,expected",
    [
        ("Производство", "Производство"),
        ("Разработки", "Разработки"),
        ("Полезное", "Полезное"),
        ("События", "События"),
        ("Наши проекты", "Наши проекты"),
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
        ("company", CategoryInvalidException),
        ("Производств", CategoryInvalidException),
    ],
)
def test_category_invalid(category_value, exception):
    with pytest.raises(exception):
        CategoryValueObject(category_value)


@pytest.mark.parametrize(
    "title_value,expected",
    [
        ("Новое поступление оборудования", "Новое поступление оборудования"),
        ("A" * 255, "A" * 255),
        ("Тестовая новость", "Тестовая новость"),
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
    "slug_value,expected",
    [
        ("novoe-postuplenie-oborudovaniya", "novoe-postuplenie-oborudovaniya"),
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
        ("invalid--slug", SlugInvalidException),
    ],
)
def test_slug_invalid(slug_value, exception):
    with pytest.raises(exception):
        SlugValueObject(slug_value)


@pytest.mark.parametrize(
    "content_value,expected",
    [
        ("Полный текст новости", "Полный текст новости"),
        ("A" * 1000, "A" * 1000),
        ("Текст с разными символами: !@#$%^&*()", "Текст с разными символами: !@#$%^&*()"),
    ],
)
def test_content_valid(content_value, expected):
    content = ContentValueObject(content_value)
    assert content.as_generic_type() == expected


@pytest.mark.parametrize(
    "content_value,exception",
    [
        ("", ContentEmptyException),
    ],
)
def test_content_invalid(content_value, exception):
    with pytest.raises(exception):
        ContentValueObject(content_value)


@pytest.mark.parametrize(
    "short_content_value,expected",
    [
        ("Краткое описание", "Краткое описание"),
        ("A" * 500, "A" * 500),
        ("Краткий текст новости", "Краткий текст новости"),
    ],
)
def test_short_content_valid(short_content_value, expected):
    short_content = ShortContentValueObject(short_content_value)
    assert short_content.as_generic_type() == expected


@pytest.mark.parametrize(
    "short_content_value,exception",
    [
        ("", ShortContentEmptyException),
        ("A" * 501, ShortContentTooLongException),
    ],
)
def test_short_content_invalid(short_content_value, exception):
    with pytest.raises(exception):
        ShortContentValueObject(short_content_value)


@pytest.mark.parametrize(
    "image_url_value,expected",
    [
        ("https://example.com/image.jpg", "https://example.com/image.jpg"),
        (None, None),
        ("http://test.ru/pic.png", "http://test.ru/pic.png"),
    ],
)
def test_image_url_valid(image_url_value, expected):
    image_url = ImageUrlValueObject(image_url_value)
    assert image_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "alt_value,expected",
    [
        ("Альтернативный текст", "Альтернативный текст"),
        ("A" * 255, "A" * 255),
        (None, None),
        ("", ""),
    ],
)
def test_alt_valid(alt_value, expected):
    alt = AltValueObject(alt_value)
    assert alt.as_generic_type() == expected


@pytest.mark.parametrize(
    "alt_value,exception",
    [
        ("A" * 256, AltTooLongException),
    ],
)
def test_alt_invalid(alt_value, exception):
    with pytest.raises(exception):
        AltValueObject(alt_value)


@pytest.mark.parametrize(
    "reading_time_value,expected",
    [
        (1, 1),
        (5, 5),
        (10, 10),
        (100, 100),
    ],
)
def test_reading_time_valid(reading_time_value, expected):
    reading_time = ReadingTimeValueObject(reading_time_value)
    assert reading_time.as_generic_type() == expected


@pytest.mark.parametrize(
    "reading_time_value,exception",
    [
        (0, ReadingTimeInvalidException),
        (-1, ReadingTimeInvalidException),
        (-10, ReadingTimeInvalidException),
    ],
)
def test_reading_time_invalid(reading_time_value, exception):
    with pytest.raises(exception):
        ReadingTimeValueObject(reading_time_value)
