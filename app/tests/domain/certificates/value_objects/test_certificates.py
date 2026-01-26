import pytest

from domain.certificates.exceptions.certificates import (
    CertificateLinkEmptyException,
    CertificateTitleEmptyException,
)
from domain.certificates.value_objects.certificates import (
    CertificateLinkValueObject,
    CertificateTitleValueObject,
)


@pytest.mark.parametrize(
    "title_value,expected",
    [
        ("Название сертификата", "Название сертификата"),
        ("Сертификат соответствия", "Сертификат соответствия"),
        ("A" * 100, "A" * 100),
    ],
)
def test_certificate_title_valid(title_value, expected):
    title = CertificateTitleValueObject(title_value)
    assert title.as_generic_type() == expected


@pytest.mark.parametrize(
    "title_value,exception",
    [
        ("", CertificateTitleEmptyException),
    ],
)
def test_certificate_title_invalid(title_value, exception):
    with pytest.raises(exception):
        CertificateTitleValueObject(title_value)


@pytest.mark.parametrize(
    "link_value,expected",
    [
        ("https://example.com/certificate.pdf", "https://example.com/certificate.pdf"),
        ("http://test.ru/doc.pdf", "http://test.ru/doc.pdf"),
        ("/path/to/certificate.pdf", "/path/to/certificate.pdf"),
        ("certificate.pdf", "certificate.pdf"),
    ],
)
def test_certificate_link_valid(link_value, expected):
    link = CertificateLinkValueObject(link_value)
    assert link.as_generic_type() == expected


@pytest.mark.parametrize(
    "link_value,exception",
    [
        ("", CertificateLinkEmptyException),
    ],
)
def test_certificate_link_invalid(link_value, exception):
    with pytest.raises(exception):
        CertificateLinkValueObject(link_value)
