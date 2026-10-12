import pytest

from domain.catalog_texts.exceptions import (
    CatalogCategoryInvalidException,
    CatalogTextContentInvalidException,
)
from domain.catalog_texts.value_objects import (
    CatalogCategoryValueObject,
    CatalogTextContentValueObject,
)


def test_category_accepts_known_slug():
    category = CatalogCategoryValueObject("transformatornye-podstancii")
    assert category.as_generic_type() == "transformatornye-podstancii"


def test_category_rejects_unknown_slug():
    with pytest.raises(CatalogCategoryInvalidException):
        CatalogCategoryValueObject("unknown")


def test_content_accepts_editor_document():
    document = {
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [{"type": "text", "text": "Заголовок"}],
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Текст "},
                    {"type": "text", "text": "жирный", "marks": [{"type": "bold"}]},
                ],
            },
            {
                "type": "orderedList",
                "attrs": {"start": 1, "type": None},
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "раз"}]},
                        ],
                    },
                ],
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "пункт"}]},
                        ],
                    },
                ],
            },
        ],
    }

    content = CatalogTextContentValueObject(document)
    assert content.as_generic_type()["type"] == "doc"


@pytest.mark.parametrize(
    "document",
    [
        {"type": "paragraph"},
        {"type": "doc", "content": [{"type": "heading", "attrs": {"level": 1}}]},
        {"type": "doc", "content": [{"type": "codeBlock"}]},
        {"type": "doc", "html": "<p>x</p>"},
    ],
)
def test_content_rejects_unsupported_document(document):
    with pytest.raises(CatalogTextContentInvalidException):
        CatalogTextContentValueObject(document)
