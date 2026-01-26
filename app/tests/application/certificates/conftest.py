import pytest
from faker import Faker

from domain.certificates.entities.certificate_groups import CertificateGroupEntity
from domain.certificates.entities.certificates import CertificateEntity
from domain.certificates.value_objects.certificate_groups import (
    ContentValueObject,
    SectionValueObject,
    TitleValueObject,
)
from domain.certificates.value_objects.certificates import (
    CertificateLinkValueObject,
    CertificateTitleValueObject,
)


@pytest.fixture
def valid_certificate_group_entity(faker: Faker) -> CertificateGroupEntity:
    return CertificateGroupEntity(
        section=SectionValueObject(value="Сертификаты"),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        content=ContentValueObject(value=faker.text(max_nb_chars=500)),
    )


@pytest.fixture
def valid_certificate_group_entity_with_section(faker: Faker):
    def _create(section: str = "Сертификаты") -> CertificateGroupEntity:
        return CertificateGroupEntity(
            section=SectionValueObject(value=section),
            title=TitleValueObject(value=faker.sentence(nb_words=5)),
            content=ContentValueObject(value=faker.text(max_nb_chars=500)),
        )

    return _create


@pytest.fixture
def valid_certificate_entity(faker: Faker) -> CertificateEntity:
    return CertificateEntity(
        title=CertificateTitleValueObject(value=faker.sentence(nb_words=3)),
        link=CertificateLinkValueObject(value=faker.url()),
        order=faker.random_int(min=0, max=100),
    )


@pytest.fixture
def valid_certificate_entity_factory(faker: Faker):
    def _create() -> CertificateEntity:
        return CertificateEntity(
            title=CertificateTitleValueObject(value=faker.sentence(nb_words=3)),
            link=CertificateLinkValueObject(value=faker.url()),
            order=faker.random_int(min=0, max=100),
        )

    return _create
