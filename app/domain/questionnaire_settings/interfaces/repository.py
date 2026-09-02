from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from domain.questionnaire_settings.entities import QuestionnaireSettingsEntity


class BaseQuestionnaireSettingsRepository(ABC):
    @abstractmethod
    async def add(self, settings: QuestionnaireSettingsEntity) -> QuestionnaireSettingsEntity: ...

    @abstractmethod
    async def get_by_id(self, settings_id: UUID) -> QuestionnaireSettingsEntity | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> QuestionnaireSettingsEntity | None: ...

    @abstractmethod
    async def update(self, settings: QuestionnaireSettingsEntity) -> None: ...

    @abstractmethod
    async def delete(self, settings_id: UUID) -> None: ...

    @abstractmethod
    async def find_all(self) -> list[QuestionnaireSettingsEntity]: ...
