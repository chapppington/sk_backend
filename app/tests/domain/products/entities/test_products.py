from uuid import uuid4

from domain.products.entities import (
    AdvantageEntity,
    DetailedDescriptionEntity,
    DocumentationEntity,
    ImportantCharacteristicEntity,
    ImportantCharacteristicUnit,
    ProductEntity,
    SimpleDescriptionEntity,
)
from domain.products.value_objects import (
    CategoryValueObject,
    DescriptionValueObject,
    NameValueObject,
    PreviewImageAltValueObject,
    PreviewImageUrlValueObject,
    SlugValueObject,
)


def test_product_entity_creation():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция 10 кВ")
    slug = SlugValueObject("transformatornaya-podstantsiya-10-kv")
    description = DescriptionValueObject("Полное описание трансформаторной подстанции")
    preview_image_url = PreviewImageUrlValueObject("https://sibkomplekt.ru/products/preview.jpg")
    preview_image_alt = PreviewImageAltValueObject("Трансформаторная подстанция")

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        preview_image_alt=preview_image_alt,
    )

    assert product.category.as_generic_type() == "Трансформаторные подстанции"
    assert product.name.as_generic_type() == "Трансформаторная подстанция 10 кВ"
    assert product.slug.as_generic_type() == "transformatornaya-podstantsiya-10-kv"
    assert product.description.as_generic_type() == "Полное описание трансформаторной подстанции"
    assert product.preview_image_url.as_generic_type() == "https://sibkomplekt.ru/products/preview.jpg"
    assert product.preview_image_alt.as_generic_type() == "Трансформаторная подстанция"
    assert product.oid is not None
    assert product.created_at is not None
    assert product.updated_at is not None
    assert product.order == 0
    assert product.is_shown is True
    assert product.show_advantages is True
    assert product.important_characteristics == []
    assert product.advantages == []
    assert product.simple_description == []
    assert product.detailed_description == []
    assert product.documentation is None
    assert product.portfolio_ids == []


def test_product_entity_creation_with_optional_fields():
    category = CategoryValueObject("Распределительные устройства среднего напряжения 6(10) кВ")
    name = NameValueObject("Распределительное устройство")
    slug = SlugValueObject("raspredelitelnoe-ustroistvo")
    description = DescriptionValueObject("Описание распределительного устройства")
    preview_image_url = PreviewImageUrlValueObject("https://sibkomplekt.ru/products/ru.jpg")
    preview_image_alt = PreviewImageAltValueObject(None)

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        preview_image_alt=preview_image_alt,
        order=5,
        is_shown=False,
        show_advantages=False,
    )

    assert product.preview_image_alt.as_generic_type() is None
    assert product.order == 5
    assert product.is_shown is False
    assert product.show_advantages is False


def test_product_entity_with_important_characteristics():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция")
    slug = SlugValueObject("transformatornaya-podstantsiya")
    description = DescriptionValueObject("Описание")
    preview_image_url = PreviewImageUrlValueObject("https://example.com/image.jpg")

    unit = ImportantCharacteristicUnit(text="кВ")
    characteristic = ImportantCharacteristicEntity(
        value="10",
        unit=unit,
        description="Номинальное напряжение",
    )

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        important_characteristics=[characteristic],
    )

    assert len(product.important_characteristics) == 1
    assert product.important_characteristics[0].value == "10"
    assert product.important_characteristics[0].unit.text == "кВ"
    assert product.important_characteristics[0].description == "Номинальное напряжение"


def test_product_entity_with_advantages():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция")
    slug = SlugValueObject("transformatornaya-podstantsiya")
    description = DescriptionValueObject("Описание")
    preview_image_url = PreviewImageUrlValueObject("https://example.com/image.jpg")

    advantage = AdvantageEntity(
        label="Надежность",
        icon="reliability-icon",
        image="https://example.com/advantage.jpg",
        alt="Надежность",
        description="Высокая надежность оборудования",
    )

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        advantages=[advantage],
    )

    assert len(product.advantages) == 1
    assert product.advantages[0].label == "Надежность"
    assert product.advantages[0].icon == "reliability-icon"
    assert product.advantages[0].image == "https://example.com/advantage.jpg"
    assert product.advantages[0].alt == "Надежность"
    assert product.advantages[0].description == "Высокая надежность оборудования"


def test_product_entity_with_simple_description():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция")
    slug = SlugValueObject("transformatornaya-podstantsiya")
    description = DescriptionValueObject("Описание")
    preview_image_url = PreviewImageUrlValueObject("https://example.com/image.jpg")

    simple_desc = SimpleDescriptionEntity(text="Простое описание товара")

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        simple_description=[simple_desc],
    )

    assert len(product.simple_description) == 1
    assert product.simple_description[0].text == "Простое описание товара"


def test_product_entity_with_detailed_description():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция")
    slug = SlugValueObject("transformatornaya-podstantsiya")
    description = DescriptionValueObject("Описание")
    preview_image_url = PreviewImageUrlValueObject("https://example.com/image.jpg")

    detailed_desc = DetailedDescriptionEntity(
        title="Технические характеристики",
        description="Детальное описание технических характеристик",
    )

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        detailed_description=[detailed_desc],
    )

    assert len(product.detailed_description) == 1
    assert product.detailed_description[0].title == "Технические характеристики"
    assert product.detailed_description[0].description == "Детальное описание технических характеристик"


def test_product_entity_with_documentation():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция")
    slug = SlugValueObject("transformatornaya-podstantsiya")
    description = DescriptionValueObject("Описание")
    preview_image_url = PreviewImageUrlValueObject("https://example.com/image.jpg")

    doc = DocumentationEntity(
        title="Руководство по эксплуатации",
        url="https://example.com/docs.pdf",
        type="pdf",
    )

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        documentation=[doc],
    )

    assert product.documentation is not None
    assert len(product.documentation) == 1
    assert product.documentation[0].title == "Руководство по эксплуатации"
    assert product.documentation[0].url == "https://example.com/docs.pdf"
    assert product.documentation[0].type == "pdf"


def test_product_entity_with_portfolio_ids():
    category = CategoryValueObject("Трансформаторные подстанции")
    name = NameValueObject("Трансформаторная подстанция")
    slug = SlugValueObject("transformatornaya-podstantsiya")
    description = DescriptionValueObject("Описание")
    preview_image_url = PreviewImageUrlValueObject("https://example.com/image.jpg")

    portfolio_id_1 = uuid4()
    portfolio_id_2 = uuid4()

    product = ProductEntity(
        category=category,
        name=name,
        slug=slug,
        description=description,
        preview_image_url=preview_image_url,
        portfolio_ids=[portfolio_id_1, portfolio_id_2],
    )

    assert len(product.portfolio_ids) == 2
    assert portfolio_id_1 in product.portfolio_ids
    assert portfolio_id_2 in product.portfolio_ids
