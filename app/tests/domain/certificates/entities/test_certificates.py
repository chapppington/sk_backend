from domain.certificates.entities import CertificateEntity
from domain.certificates.value_objects.certificates import (
    CertificateLinkValueObject,
    CertificateTitleValueObject,
)


def test_certificate_entity_creation():
    title = CertificateTitleValueObject("Сертификат соответствия ГОСТ Р")
    link = CertificateLinkValueObject("https://example.com/certificate.pdf")
    order = 1

    certificate = CertificateEntity(
        title=title,
        link=link,
        order=order,
    )

    assert certificate.title.as_generic_type() == "Сертификат соответствия ГОСТ Р"
    assert certificate.link.as_generic_type() == "https://example.com/certificate.pdf"
    assert certificate.order == 1
    assert certificate.oid is not None
    assert certificate.created_at is not None
    assert certificate.updated_at is not None


def test_certificate_entity_creation_with_different_links():
    test_cases = [
        ("https://example.com/cert.pdf", 1),
        ("http://test.ru/document.pdf", 2),
        ("/path/to/certificate.pdf", 3),
        ("certificate.pdf", 4),
    ]

    for link_value, order_value in test_cases:
        title = CertificateTitleValueObject(f"Сертификат {order_value}")
        link = CertificateLinkValueObject(link_value)

        certificate = CertificateEntity(
            title=title,
            link=link,
            order=order_value,
        )

        assert certificate.title.as_generic_type() == f"Сертификат {order_value}"
        assert certificate.link.as_generic_type() == link_value
        assert certificate.order == order_value
        assert certificate.oid is not None
