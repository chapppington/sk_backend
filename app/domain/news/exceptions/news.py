from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class NewsException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с новостями"


@dataclass(eq=False)
class CategoryInvalidException(NewsException):
    category: str

    @property
    def message(self) -> str:
        return f"Недопустимая категория: {self.category}"


@dataclass(eq=False)
class TitleEmptyException(NewsException):
    @property
    def message(self) -> str:
        return "Заголовок не может быть пустым"


@dataclass(eq=False)
class TitleTooLongException(NewsException):
    title_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Заголовок слишком длинный. Текущая длина: {self.title_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class SlugEmptyException(NewsException):
    @property
    def message(self) -> str:
        return "Slug не может быть пустым"


@dataclass(eq=False)
class SlugInvalidException(NewsException):
    slug: str

    @property
    def message(self) -> str:
        return f"Недопустимый формат slug: {self.slug}"


@dataclass(eq=False)
class ContentEmptyException(NewsException):
    @property
    def message(self) -> str:
        return "Содержание не может быть пустым"


@dataclass(eq=False)
class ShortContentEmptyException(NewsException):
    @property
    def message(self) -> str:
        return "Краткое содержание не может быть пустым"


@dataclass(eq=False)
class ShortContentTooLongException(NewsException):
    content_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Краткое содержание слишком длинное. Текущая длина: {self.content_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class ReadingTimeInvalidException(NewsException):
    reading_time: int

    @property
    def message(self) -> str:
        return f"Недопустимое время чтения: {self.reading_time}. Должно быть положительным числом"


@dataclass(eq=False)
class AltTooLongException(NewsException):
    alt_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Альтернативный текст слишком длинный. Текущая длина: {self.alt_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class NewsNotFoundException(NewsException):
    news_id: UUID

    @property
    def message(self) -> str:
        return f"Новость с id {self.news_id} не найдена"


@dataclass(eq=False)
class NewsNotFoundBySlugException(NewsException):
    slug: str

    @property
    def message(self) -> str:
        return f"Новость со slug '{self.slug}' не найдена"


@dataclass(eq=False)
class NewsAlreadyExistsException(NewsException):
    slug: str

    @property
    def message(self) -> str:
        return f"Новость со slug '{self.slug}' уже существует"
