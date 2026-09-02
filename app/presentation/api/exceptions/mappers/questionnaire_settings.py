from fastapi import status

from domain.questionnaire_settings.exceptions.questionnaire_settings import (
    QuestionnaireSettingsAlreadyExistsException,
    QuestionnaireSettingsException,
    QuestionnaireSettingsNotFoundException,
)


def map_questionnaire_settings_exception_to_status_code(
    exc: QuestionnaireSettingsException,
) -> int:
    if isinstance(exc, QuestionnaireSettingsNotFoundException):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, QuestionnaireSettingsAlreadyExistsException):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST
