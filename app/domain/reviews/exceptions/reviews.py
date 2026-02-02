from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class ReviewException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с отзывами"


@dataclass(eq=False)
class ReviewNameEmptyException(ReviewException):
    @property
    def message(self) -> str:
        return "Имя в отзыве не может быть пустым"


@dataclass(eq=False)
class ReviewTextEmptyException(ReviewException):
    @property
    def message(self) -> str:
        return "Текст отзыва сотрудника не может быть пустым"


@dataclass(eq=False)
class ReviewShortTextEmptyException(ReviewException):
    @property
    def message(self) -> str:
        return "Короткий текст отзыва сотрудника не может быть пустым"


@dataclass(eq=False)
class ReviewContentUrlEmptyException(ReviewException):
    @property
    def message(self) -> str:
        return "URL контента отзыва клиента не может быть пустым"


@dataclass(eq=False)
class ReviewCategoryInvalidException(ReviewException):
    category: str

    @property
    def message(self) -> str:
        return f"Недопустимая категория отзыва: {self.category}"


@dataclass(eq=False)
class ReviewNotFoundException(ReviewException):
    review_id: UUID

    @property
    def message(self) -> str:
        return f"Отзыв с id {self.review_id} не найден"
