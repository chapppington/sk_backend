from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class SubmissionException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с заявками"


@dataclass(eq=False)
class FormTypeInvalidException(SubmissionException):
    form_type: str

    @property
    def message(self) -> str:
        return f"Недопустимый тип формы: {self.form_type}"


@dataclass(eq=False)
class QuestionnaireTypeInvalidException(SubmissionException):
    questionnaire_type: str

    @property
    def message(self) -> str:
        return f"Недопустимый тип опросного листа: {self.questionnaire_type}"


@dataclass(eq=False)
class NameEmptyException(SubmissionException):
    @property
    def message(self) -> str:
        return "Имя не может быть пустым"


@dataclass(eq=False)
class EmailInvalidException(SubmissionException):
    email: str

    @property
    def message(self) -> str:
        return f"Недопустимый email: {self.email}"


@dataclass(eq=False)
class SubmissionNotFoundException(SubmissionException):
    submission_id: UUID

    @property
    def message(self) -> str:
        return f"Заявка с id {self.submission_id} не найдена"
