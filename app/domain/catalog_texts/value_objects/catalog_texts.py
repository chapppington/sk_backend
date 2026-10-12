from dataclasses import dataclass
from typing import Any

from domain.base.value_object import BaseValueObject
from domain.catalog_texts.exceptions import (
    CatalogCategoryInvalidException,
    CatalogTextContentInvalidException,
)


VALID_CATALOG_CATEGORIES = frozenset(
    {
        "transformatornye-podstancii",
        "raspredelitelnye-ustroystva-srednego-napryazheniya-6-10-kv",
        "raspredelitelnye-ustroystva-nizkogo-napryazheniya-04-kv",
        "punkty-ucheta-i-sekcionirovaniya-vle",
        "elektrostancii-i-ustanovki",
    },
)

_ALLOWED_NODE_TYPES = frozenset(
    {
        "doc",
        "paragraph",
        "heading",
        "text",
        "bulletList",
        "orderedList",
        "listItem",
        "hardBreak",
    },
)
_ALLOWED_MARK_TYPES = frozenset({"bold", "italic"})
_ALLOWED_NODE_KEYS = frozenset({"type", "content", "text", "marks", "attrs"})
_MAX_DEPTH = 12
_MAX_NODES = 500


def _invalid(reason: str) -> CatalogTextContentInvalidException:
    return CatalogTextContentInvalidException(reason=reason)


def _validate_marks(marks: Any) -> None:
    if not isinstance(marks, list):
        raise _invalid("пометки текста должны быть списком")

    for mark in marks:
        if not isinstance(mark, dict):
            raise _invalid("пометка текста имеет неверный формат")
        if set(mark) - {"type", "attrs"}:
            raise _invalid("в пометке текста есть лишние поля")
        if mark.get("type") not in _ALLOWED_MARK_TYPES:
            raise _invalid("разрешены только пометки bold и italic")
        attrs = mark.get("attrs")
        if attrs is not None and attrs != {}:
            raise _invalid("у пометок текста не должно быть атрибутов")


def _validate_attrs(node_type: str, attrs: Any) -> None:
    if attrs is None:
        return
    if not isinstance(attrs, dict):
        raise _invalid("атрибуты узла должны быть объектом")

    if node_type == "heading":
        if set(attrs) - {"level"}:
            raise _invalid("у заголовка допустим только уровень")
        if attrs.get("level", 2) not in (2, 3):
            raise _invalid("заголовок может быть только h2 или h3")
        return

    if node_type == "orderedList":
        if set(attrs) - {"start"}:
            raise _invalid("у нумерованного списка допустим только start")
        start = attrs.get("start", 1)
        if isinstance(start, bool) or not isinstance(start, int) or start < 1:
            raise _invalid("start нумерованного списка должен быть целым числом от 1")
        return

    if attrs != {}:
        raise _invalid(f"у узла {node_type} не должно быть атрибутов")


def _validate_node(node: Any, depth: int, counter: list[int]) -> None:
    counter[0] += 1
    if counter[0] > _MAX_NODES:
        raise _invalid("документ слишком большой")
    if depth > _MAX_DEPTH:
        raise _invalid("документ слишком глубоко вложен")
    if not isinstance(node, dict):
        raise _invalid("узел документа должен быть объектом")
    if not set(node).issubset(_ALLOWED_NODE_KEYS):
        raise _invalid("в узле документа есть лишние поля")

    node_type = node.get("type")
    if node_type not in _ALLOWED_NODE_TYPES:
        raise _invalid("в документе есть неподдерживаемый блок")

    _validate_attrs(node_type, node.get("attrs"))

    if node_type == "text":
        if not isinstance(node.get("text"), str):
            raise _invalid("текстовый узел должен содержать строку")
        if node.get("content"):
            raise _invalid("текстовый узел не может содержать вложенные блоки")
        _validate_marks(node.get("marks", []))
        return

    if node.get("text") is not None or node.get("marks") is not None:
        raise _invalid("текст и пометки допустимы только в текстовом узле")

    content = node.get("content", [])
    if not isinstance(content, list):
        raise _invalid("вложенные блоки должны быть списком")
    if node_type == "hardBreak" and content:
        raise _invalid("перенос строки не может содержать вложенные блоки")

    for child in content:
        _validate_node(child, depth + 1, counter)


def validate_catalog_text_document(value: Any) -> dict:
    if not isinstance(value, dict) or value.get("type") != "doc":
        raise _invalid("корнем документа должен быть узел doc")
    _validate_node(value, 0, [0])
    return value


@dataclass(frozen=True)
class CatalogCategoryValueObject(BaseValueObject):
    value: str

    def validate(self):
        category = self.value.strip().lower()
        if category not in VALID_CATALOG_CATEGORIES:
            raise CatalogCategoryInvalidException(category=self.value)

    def as_generic_type(self) -> str:
        return self.value.strip().lower()


@dataclass(frozen=True)
class CatalogTextContentValueObject(BaseValueObject):
    value: dict

    def validate(self):
        validate_catalog_text_document(self.value)

    def as_generic_type(self) -> dict:
        return self.value
