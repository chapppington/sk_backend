from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class PortfolioException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с портфолио"


@dataclass(eq=False)
class NameEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Название не может быть пустым"


@dataclass(eq=False)
class NameTooLongException(PortfolioException):
    name_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Название слишком длинное. Текущая длина: {self.name_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class SlugEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Slug не может быть пустым"


@dataclass(eq=False)
class SlugInvalidException(PortfolioException):
    slug: str

    @property
    def message(self) -> str:
        return f"Недопустимый slug: {self.slug}. Slug должен содержать только буквы, цифры, дефисы и подчеркивания"


@dataclass(eq=False)
class PosterUrlInvalidException(PortfolioException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый URL постера: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class YearInvalidException(PortfolioException):
    year: int

    @property
    def message(self) -> str:
        return f"Недопустимый год: {self.year}. Год должен быть между 2000 и 2100"


@dataclass(eq=False)
class TaskTitleEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Заголовок задачи не может быть пустым"


@dataclass(eq=False)
class TaskDescriptionEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Описание задачи не может быть пустым"


@dataclass(eq=False)
class SolutionTitleEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Заголовок решения не может быть пустым"


@dataclass(eq=False)
class SolutionDescriptionEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Описание решения не может быть пустым"


@dataclass(eq=False)
class SolutionSubtitleEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Подзаголовок решения не может быть пустым"


@dataclass(eq=False)
class SolutionSubdescriptionEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Подописание решения не может быть пустым"


@dataclass(eq=False)
class SolutionImageUrlInvalidException(PortfolioException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый URL изображения решения: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class VideoUrlInvalidException(PortfolioException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый URL видео: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class ReviewImageUrlInvalidException(PortfolioException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый URL изображения отзыва: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class DescriptionEmptyException(PortfolioException):
    @property
    def message(self) -> str:
        return "Описание не может быть пустым"


@dataclass(eq=False)
class PortfolioNotFoundException(PortfolioException):
    portfolio_id: UUID

    @property
    def message(self) -> str:
        return f"Портфолио с id {self.portfolio_id} не найдено"


@dataclass(eq=False)
class PortfolioNotFoundBySlugException(PortfolioException):
    slug: str

    @property
    def message(self) -> str:
        return f"Портфолио со slug '{self.slug}' не найдено"


@dataclass(eq=False)
class PortfolioAlreadyExistsException(PortfolioException):
    slug: str

    @property
    def message(self) -> str:
        return f"Портфолио со slug '{self.slug}' уже существует"
