import pytest

from domain.products.exceptions import (
    CategoryInvalidException,
    DescriptionEmptyException,
    NameEmptyException,
    NameTooLongException,
    PreviewImageUrlInvalidException,
    SlugEmptyException,
    SlugInvalidException,
)
from domain.products.value_objects.products import (
    CategoryValueObject,
    DescriptionValueObject,
    NameValueObject,
    PreviewImageAltValueObject,
    PreviewImageUrlValueObject,
    SlugValueObject,
)


@pytest.mark.parametrize(
    "name_value,expected",
    [
        ("Трансформаторная подстанция 10 кВ", "Трансформаторная подстанция 10 кВ"),
        ("A" * 255, "A" * 255),
        ("Распределительное устройство", "Распределительное устройство"),
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
        ("transformatornaya-podstantsiya-10-kv", "transformatornaya-podstantsiya-10-kv"),
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
        ("A" * 256, SlugInvalidException),
    ],
)
def test_slug_invalid(slug_value, exception):
    with pytest.raises(exception):
        SlugValueObject(slug_value)


@pytest.mark.parametrize(
    "description_value,expected",
    [
        ("Полное описание товара", "Полное описание товара"),
        ("A" * 1000, "A" * 1000),
        ("Описание с разными символами: !@#$%^&*()", "Описание с разными символами: !@#$%^&*()"),
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
    "category_value,expected",
    [
        ("Трансформаторные подстанции", "Трансформаторные подстанции"),
        (
            "Распределительные устройства среднего напряжения 6(10) кВ",
            "Распределительные устройства среднего напряжения 6(10) кВ",
        ),
        (
            "Распределительные устройства низкого напряжения 0,4 кВ",
            "Распределительные устройства низкого напряжения 0,4 кВ",
        ),
        (
            "Пункты коммерческого учёта и секционирования воздушных линий электропередач",
            "Пункты коммерческого учёта и секционирования воздушных линий электропередач",
        ),
        ("Электростанции и установки", "Электростанции и установки"),
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
        ("Трансформаторные", CategoryInvalidException),
        ("Производство", CategoryInvalidException),
    ],
)
def test_category_invalid(category_value, exception):
    with pytest.raises(exception):
        CategoryValueObject(category_value)


@pytest.mark.parametrize(
    "preview_image_url_value,expected",
    [
        ("https://example.com/image.jpg", "https://example.com/image.jpg"),
        ("http://test.ru/pic.png", "http://test.ru/pic.png"),
        ("https://sibkomplekt.ru/products/preview.jpg", "https://sibkomplekt.ru/products/preview.jpg"),
    ],
)
def test_preview_image_url_valid(preview_image_url_value, expected):
    preview_image_url = PreviewImageUrlValueObject(preview_image_url_value)
    assert preview_image_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "preview_image_url_value,exception",
    [
        ("", PreviewImageUrlInvalidException),
        ("invalid-url", PreviewImageUrlInvalidException),
        ("ftp://example.com/image.jpg", PreviewImageUrlInvalidException),
        ("/relative/path/image.jpg", PreviewImageUrlInvalidException),
        ("example.com/image.jpg", PreviewImageUrlInvalidException),
    ],
)
def test_preview_image_url_invalid(preview_image_url_value, exception):
    with pytest.raises(exception):
        PreviewImageUrlValueObject(preview_image_url_value)


@pytest.mark.parametrize(
    "preview_image_alt_value,expected",
    [
        ("Альтернативный текст изображения", "Альтернативный текст изображения"),
        ("", ""),
        (None, None),
    ],
)
def test_preview_image_alt_valid(preview_image_alt_value, expected):
    preview_image_alt = PreviewImageAltValueObject(preview_image_alt_value)
    assert preview_image_alt.as_generic_type() == expected
