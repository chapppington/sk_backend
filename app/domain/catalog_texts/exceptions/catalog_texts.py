from dataclasses import dataclass

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class CatalogTextException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с SEO-текстом категории"


@dataclass(eq=False)
class CatalogCategoryInvalidException(CatalogTextException):
    category: str

    @property
    def message(self) -> str:
        category_label = self.category.strip() or "пустая"
        return f"Недопустимая категория каталога: «{category_label}»"


@dataclass(eq=False)
class CatalogTextContentInvalidException(CatalogTextException):
    reason: str = "содержимое не похоже на документ редактора"

    @property
    def message(self) -> str:
        return f"Недопустимый SEO-текст: {self.reason}"


@dataclass(eq=False)
class CatalogTextNotFoundException(CatalogTextException):
    category: str

    @property
    def message(self) -> str:
        return f"SEO-текст для категории '{self.category}' не найден"
