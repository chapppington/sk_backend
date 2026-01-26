import pytest
from faker import Faker

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


@pytest.fixture
def valid_seo_settings_entity(faker: Faker) -> SeoSettingsEntity:
    return SeoSettingsEntity(
        page_path=PagePathValueObject(value=f"/{faker.slug()}"),
        page_name=PageNameValueObject(value=faker.sentence(nb_words=3)),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        description=DescriptionValueObject(value=faker.text(max_nb_chars=500)),
    )


@pytest.fixture
def valid_seo_settings_entity_with_optional_fields(faker: Faker) -> SeoSettingsEntity:
    return SeoSettingsEntity(
        page_path=PagePathValueObject(value=f"/{faker.slug()}"),
        page_name=PageNameValueObject(value=faker.sentence(nb_words=3)),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        description=DescriptionValueObject(value=faker.text(max_nb_chars=500)),
        keywords=KeywordsValueObject(value=faker.sentence(nb_words=5)),
        og_title=OgTitleValueObject(value=faker.sentence(nb_words=5)),
        og_description=OgDescriptionValueObject(value=faker.text(max_nb_chars=200)),
        og_image=OgImageValueObject(value=faker.image_url()),
        canonical_url=CanonicalUrlValueObject(value=faker.url()),
        is_active=True,
    )
