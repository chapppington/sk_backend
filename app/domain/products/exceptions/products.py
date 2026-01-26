from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class ProductException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с товаром"


@dataclass(eq=False)
class NameEmptyException(ProductException):
    @property
    def message(self) -> str:
        return "Название не может быть пустым"


@dataclass(eq=False)
class NameTooLongException(ProductException):
    name_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Название слишком длинное. Текущая длина: {self.name_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class SlugEmptyException(ProductException):
    @property
    def message(self) -> str:
        return "Slug не может быть пустым"


@dataclass(eq=False)
class SlugInvalidException(ProductException):
    slug: str

    @property
    def message(self) -> str:
        return f"Недопустимый slug: {self.slug}. Slug должен содержать только буквы, цифры и дефисы"


@dataclass(eq=False)
class DescriptionEmptyException(ProductException):
    @property
    def message(self) -> str:
        return "Описание не может быть пустым"


@dataclass(eq=False)
class CategoryInvalidException(ProductException):
    category: str

    @property
    def message(self) -> str:
        return f"Недопустимая категория: {self.category}"


@dataclass(eq=False)
class PreviewImageUrlInvalidException(ProductException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый URL превью изображения: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class OrderInvalidException(ProductException):
    order: int

    @property
    def message(self) -> str:
        return f"Недопустимый порядок: {self.order}. Порядок должен быть неотрицательным числом"


@dataclass(eq=False)
class ProductNotFoundException(ProductException):
    product_id: UUID

    @property
    def message(self) -> str:
        return f"Товар с id {self.product_id} не найден"


@dataclass(eq=False)
class ProductNotFoundBySlugException(ProductException):
    slug: str

    @property
    def message(self) -> str:
        return f"Товар со slug '{self.slug}' не найден"


@dataclass(eq=False)
class ProductAlreadyExistsException(ProductException):
    slug: str

    @property
    def message(self) -> str:
        return f"Товар со slug '{self.slug}' уже существует"
