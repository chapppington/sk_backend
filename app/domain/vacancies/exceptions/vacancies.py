from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class VacancyException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с вакансиями"


@dataclass(eq=False)
class CategoryInvalidException(VacancyException):
    category: str

    @property
    def message(self) -> str:
        return f"Недопустимая категория: {self.category}"


@dataclass(eq=False)
class TitleEmptyException(VacancyException):
    @property
    def message(self) -> str:
        return "Заголовок не может быть пустым"


@dataclass(eq=False)
class TitleTooLongException(VacancyException):
    title_length: int
    max_length: int

    @property
    def message(self) -> str:
        return (
            f"Заголовок слишком длинный. Текущая длина: {self.title_length}, "
            f"максимально допустимая длина: {self.max_length}"
        )


@dataclass(eq=False)
class RequirementsEmptyException(VacancyException):
    @property
    def message(self) -> str:
        return "Требования не могут быть пустыми"


@dataclass(eq=False)
class ExperienceEmptyException(VacancyException):
    @property
    def message(self) -> str:
        return "Опыт работы не может быть пустым"


@dataclass(eq=False)
class SalaryInvalidException(VacancyException):
    salary: int

    @property
    def message(self) -> str:
        return f"Недопустимая зарплата: {self.salary}. Должна быть неотрицательным числом"


@dataclass(eq=False)
class VacancyNotFoundException(VacancyException):
    vacancy_id: UUID

    @property
    def message(self) -> str:
        return f"Вакансия с id {self.vacancy_id} не найдена"


@dataclass(eq=False)
class VacancyAlreadyExistsException(VacancyException):
    title: str

    @property
    def message(self) -> str:
        return f"Вакансия с заголовком '{self.title}' уже существует"
