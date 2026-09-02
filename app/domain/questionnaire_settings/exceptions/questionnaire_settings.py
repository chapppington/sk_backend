from dataclasses import dataclass

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class QuestionnaireSettingsException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с настройками опросных листов"


@dataclass(eq=False)
class QuestionnaireSlugInvalidException(QuestionnaireSettingsException):
    slug: str

    @property
    def message(self) -> str:
        slug_label = self.slug.strip() or "пустой"
        return (
            f"Недопустимый slug: «{slug_label}». "
            "Используйте латиницу, цифры и дефисы (например: ktp, krun)"
        )


@dataclass(eq=False)
class QuestionnaireH1EmptyException(QuestionnaireSettingsException):
    @property
    def message(self) -> str:
        return "Заголовок H1 не может быть пустым"


@dataclass(eq=False)
class PageNameEmptyException(QuestionnaireSettingsException):
    @property
    def message(self) -> str:
        return "Название страницы не может быть пустым"


@dataclass(eq=False)
class QuestionnaireSettingsNotFoundException(QuestionnaireSettingsException):
    slug: str | None = None
    questionnaire_settings_id: str | None = None

    @property
    def message(self) -> str:
        if self.slug:
            return f"Настройки опросного листа '{self.slug}' не найдены"
        return f"Настройки опросного листа с id {self.questionnaire_settings_id} не найдены"


@dataclass(eq=False)
class QuestionnaireSettingsAlreadyExistsException(QuestionnaireSettingsException):
    slug: str

    @property
    def message(self) -> str:
        return f"Опросный лист со slug '{self.slug}' уже существует"
