from domain.seo_settings.entities import SeoSettingsEntity
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


def test_seo_settings_entity_creation():
    page_path = PagePathValueObject("/about")
    page_name = PageNameValueObject("О компании")
    title = TitleValueObject("О компании - Сибирский Комплект")
    description = DescriptionValueObject("Узнайте больше о компании Сибирский Комплект")

    seo_settings = SeoSettingsEntity(
        page_path=page_path,
        page_name=page_name,
        title=title,
        description=description,
    )

    assert seo_settings.page_path.as_generic_type() == "/about"
    assert seo_settings.page_name.as_generic_type() == "О компании"
    assert seo_settings.title.as_generic_type() == "О компании - Сибирский Комплект"
    assert seo_settings.description.as_generic_type() == "Узнайте больше о компании Сибирский Комплект"
    assert seo_settings.keywords is None
    assert seo_settings.og_title is None
    assert seo_settings.og_description is None
    assert seo_settings.og_image is None
    assert seo_settings.canonical_url is None
    assert seo_settings.is_active is True
    assert seo_settings.oid is not None
    assert seo_settings.created_at is not None
    assert seo_settings.updated_at is not None


def test_seo_settings_entity_creation_with_optional_fields():
    page_path = PagePathValueObject("/products")
    page_name = PageNameValueObject("Продукты")
    title = TitleValueObject("Продукты - Сибирский Комплект")
    description = DescriptionValueObject("Наши продукты")
    keywords = KeywordsValueObject("продукты, оборудование")
    og_title = OgTitleValueObject("Продукты - Сибирский Комплект")
    og_description = OgDescriptionValueObject("Описание продуктов для Open Graph")
    og_image = OgImageValueObject("https://sibkomplekt.ru/images/og-products.jpg")
    canonical_url = CanonicalUrlValueObject("https://sibkomplekt.ru/products")

    seo_settings = SeoSettingsEntity(
        page_path=page_path,
        page_name=page_name,
        title=title,
        description=description,
        keywords=keywords,
        og_title=og_title,
        og_description=og_description,
        og_image=og_image,
        canonical_url=canonical_url,
        is_active=False,
    )

    assert seo_settings.page_path.as_generic_type() == "/products"
    assert seo_settings.keywords.as_generic_type() == "продукты, оборудование"
    assert seo_settings.og_title.as_generic_type() == "Продукты - Сибирский Комплект"
    assert seo_settings.og_description.as_generic_type() == "Описание продуктов для Open Graph"
    assert seo_settings.og_image.as_generic_type() == "https://sibkomplekt.ru/images/og-products.jpg"
    assert seo_settings.canonical_url.as_generic_type() == "https://sibkomplekt.ru/products"
    assert seo_settings.is_active is False


def test_seo_settings_entity_creation_with_none_optional_fields():
    page_path = PagePathValueObject("/contact")
    page_name = PageNameValueObject("Контакты")
    title = TitleValueObject("Контакты - Сибирский Комплект")
    description = DescriptionValueObject("Свяжитесь с нами")

    seo_settings = SeoSettingsEntity(
        page_path=page_path,
        page_name=page_name,
        title=title,
        description=description,
        keywords=None,
        og_title=None,
        og_description=None,
        og_image=None,
        canonical_url=None,
    )

    assert seo_settings.keywords is None
    assert seo_settings.og_title is None
    assert seo_settings.og_description is None
    assert seo_settings.og_image is None
    assert seo_settings.canonical_url is None
    assert seo_settings.is_active is True
