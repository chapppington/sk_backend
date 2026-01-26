import pytest

from domain.seo_settings.exceptions import (
    CanonicalUrlInvalidException,
    OgImageUrlInvalidException,
    PageNameEmptyException,
    PagePathEmptyException,
    PagePathInvalidException,
    TitleEmptyException,
)
from domain.seo_settings.value_objects import (
    CanonicalUrlValueObject,
    DescriptionValueObject,
    KeywordsValueObject,
    OgDescriptionValueObject,
    OgImageValueObject,
    OgTitleValueObject,
    PageNameValueObject,
    PagePathValueObject,
    TitleValueObject,
)


@pytest.mark.parametrize(
    "page_path_value,expected",
    [
        ("/about", "/about"),
        ("/products", "/products"),
        ("/", "/"),
        ("/very/long/path/to/page", "/very/long/path/to/page"),
    ],
)
def test_page_path_valid(page_path_value, expected):
    page_path = PagePathValueObject(page_path_value)
    assert page_path.as_generic_type() == expected


@pytest.mark.parametrize(
    "page_path_value,exception",
    [
        ("", PagePathEmptyException),
        ("about", PagePathInvalidException),
        ("about/", PagePathInvalidException),
        ("/about/", PagePathInvalidException),
    ],
)
def test_page_path_invalid(page_path_value, exception):
    with pytest.raises(exception):
        PagePathValueObject(page_path_value)


@pytest.mark.parametrize(
    "page_name_value,expected",
    [
        ("О компании", "О компании"),
        ("Главная страница", "Главная страница"),
        ("A" * 100, "A" * 100),
    ],
)
def test_page_name_valid(page_name_value, expected):
    page_name = PageNameValueObject(page_name_value)
    assert page_name.as_generic_type() == expected


@pytest.mark.parametrize(
    "page_name_value,exception",
    [
        ("", PageNameEmptyException),
    ],
)
def test_page_name_invalid(page_name_value, exception):
    with pytest.raises(exception):
        PageNameValueObject(page_name_value)


@pytest.mark.parametrize(
    "title_value,expected",
    [
        ("О компании - Сибирский Комплект", "О компании - Сибирский Комплект"),
        ("Главная страница", "Главная страница"),
        ("A" * 255, "A" * 255),
    ],
)
def test_title_valid(title_value, expected):
    title = TitleValueObject(title_value)
    assert title.as_generic_type() == expected


@pytest.mark.parametrize(
    "title_value,exception",
    [
        ("", TitleEmptyException),
    ],
)
def test_title_invalid(title_value, exception):
    with pytest.raises(exception):
        TitleValueObject(title_value)


@pytest.mark.parametrize(
    "description_value,expected",
    [
        ("Описание страницы", "Описание страницы"),
        ("", ""),
        ("A" * 1000, "A" * 1000),
    ],
)
def test_description_valid(description_value, expected):
    description = DescriptionValueObject(description_value)
    assert description.as_generic_type() == expected


@pytest.mark.parametrize(
    "keywords_value,expected",
    [
        ("о компании, сибирский комплект", "о компании, сибирский комплект"),
        ("", ""),
        (None, None),
    ],
)
def test_keywords_valid(keywords_value, expected):
    keywords = KeywordsValueObject(keywords_value)
    assert keywords.as_generic_type() == expected


@pytest.mark.parametrize(
    "og_title_value,expected",
    [
        ("О компании - Сибирский Комплект", "О компании - Сибирский Комплект"),
        ("", ""),
        (None, None),
    ],
)
def test_og_title_valid(og_title_value, expected):
    og_title = OgTitleValueObject(og_title_value)
    assert og_title.as_generic_type() == expected


@pytest.mark.parametrize(
    "og_description_value,expected",
    [
        ("Описание для Open Graph", "Описание для Open Graph"),
        ("", ""),
        (None, None),
    ],
)
def test_og_description_valid(og_description_value, expected):
    og_description = OgDescriptionValueObject(og_description_value)
    assert og_description.as_generic_type() == expected


@pytest.mark.parametrize(
    "og_image_value,expected",
    [
        ("https://sibkomplekt.ru/images/og-about.jpg", "https://sibkomplekt.ru/images/og-about.jpg"),
        ("http://example.com/image.jpg", "http://example.com/image.jpg"),
        (None, None),
    ],
)
def test_og_image_valid(og_image_value, expected):
    og_image = OgImageValueObject(og_image_value)
    assert og_image.as_generic_type() == expected


@pytest.mark.parametrize(
    "og_image_value,exception",
    [
        ("invalid-url", OgImageUrlInvalidException),
        ("ftp://example.com/image.jpg", OgImageUrlInvalidException),
        ("/relative/path/image.jpg", OgImageUrlInvalidException),
        ("example.com/image.jpg", OgImageUrlInvalidException),
    ],
)
def test_og_image_invalid(og_image_value, exception):
    with pytest.raises(exception):
        OgImageValueObject(og_image_value)


@pytest.mark.parametrize(
    "canonical_url_value,expected",
    [
        ("https://sibkomplekt.ru/about", "https://sibkomplekt.ru/about"),
        ("http://example.com/page", "http://example.com/page"),
        (None, None),
    ],
)
def test_canonical_url_valid(canonical_url_value, expected):
    canonical_url = CanonicalUrlValueObject(canonical_url_value)
    assert canonical_url.as_generic_type() == expected


@pytest.mark.parametrize(
    "canonical_url_value,exception",
    [
        ("invalid-url", CanonicalUrlInvalidException),
        ("ftp://example.com/page", CanonicalUrlInvalidException),
        ("/relative/path", CanonicalUrlInvalidException),
        ("example.com/page", CanonicalUrlInvalidException),
    ],
)
def test_canonical_url_invalid(canonical_url_value, exception):
    with pytest.raises(exception):
        CanonicalUrlValueObject(canonical_url_value)
