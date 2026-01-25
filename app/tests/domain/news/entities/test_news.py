from datetime import datetime
from uuid import uuid4

from domain.news.entities import NewsEntity
from domain.news.value_objects import (
    AltValueObject,
    CategoryValueObject,
    ContentValueObject,
    ImageUrlValueObject,
    ReadingTimeValueObject,
    ShortContentValueObject,
    SlugValueObject,
    TitleValueObject,
)


def test_news_entity_creation():
    category = CategoryValueObject("Производство")
    title = TitleValueObject("Новое поступление оборудования")
    slug = SlugValueObject("novoe-postuplenie-oborudovaniya")
    content = ContentValueObject("Полный текст новости с подробным описанием...")
    short_content = ShortContentValueObject("Краткое описание новости для превью")
    image_url = ImageUrlValueObject("https://sibkomplekt.ru/images/news/equipment.jpg")
    alt = AltValueObject("Новое оборудование на складе")
    reading_time = ReadingTimeValueObject(5)
    date = datetime(2026, 1, 20, 14, 0, 0)

    news = NewsEntity(
        category=category,
        title=title,
        slug=slug,
        content=content,
        short_content=short_content,
        image_url=image_url,
        alt=alt,
        reading_time=reading_time,
        date=date,
    )

    assert news.category.as_generic_type() == "Производство"
    assert news.title.as_generic_type() == "Новое поступление оборудования"
    assert news.slug.as_generic_type() == "novoe-postuplenie-oborudovaniya"
    assert news.content.as_generic_type() == "Полный текст новости с подробным описанием..."
    assert news.short_content.as_generic_type() == "Краткое описание новости для превью"
    assert news.image_url.as_generic_type() == "https://sibkomplekt.ru/images/news/equipment.jpg"
    assert news.alt.as_generic_type() == "Новое оборудование на складе"
    assert news.reading_time.as_generic_type() == 5
    assert news.date == date
    assert news.oid is not None
    assert news.created_at is not None
    assert news.updated_at is not None


def test_news_entity_creation_with_optional_fields():
    category = CategoryValueObject("События")
    title = TitleValueObject("Тестовая новость")
    slug = SlugValueObject("testovaya-novost")
    content = ContentValueObject("Полный текст")
    short_content = ShortContentValueObject("Краткое описание")
    image_url = ImageUrlValueObject(None)
    alt = AltValueObject(None)
    reading_time = ReadingTimeValueObject(3)
    date = datetime(2026, 1, 20, 14, 0, 0)

    news = NewsEntity(
        category=category,
        title=title,
        slug=slug,
        content=content,
        short_content=short_content,
        image_url=image_url,
        alt=alt,
        reading_time=reading_time,
        date=date,
    )

    assert news.image_url.as_generic_type() is None
    assert news.alt.as_generic_type() is None


def test_news_entity_equality():
    news_id = uuid4()
    category = CategoryValueObject("Производство")
    title = TitleValueObject("Тестовая новость")
    slug = SlugValueObject("testovaya-novost")
    content = ContentValueObject("Полный текст")
    short_content = ShortContentValueObject("Краткое описание")
    image_url = ImageUrlValueObject(None)
    alt = AltValueObject(None)
    reading_time = ReadingTimeValueObject(5)
    date = datetime(2026, 1, 20, 14, 0, 0)

    news1 = NewsEntity(
        oid=news_id,
        category=category,
        title=title,
        slug=slug,
        content=content,
        short_content=short_content,
        image_url=image_url,
        alt=alt,
        reading_time=reading_time,
        date=date,
    )

    news2 = NewsEntity(
        oid=news_id,
        category=category,
        title=title,
        slug=slug,
        content=content,
        short_content=short_content,
        image_url=image_url,
        alt=alt,
        reading_time=reading_time,
        date=date,
    )

    news3 = NewsEntity(
        oid=uuid4(),
        category=category,
        title=title,
        slug=slug,
        content=content,
        short_content=short_content,
        image_url=image_url,
        alt=alt,
        reading_time=reading_time,
        date=date,
    )

    assert news1 == news2
    assert news1 != news3
