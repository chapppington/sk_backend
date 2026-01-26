from dataclasses import dataclass
from uuid import UUID

from domain.base.exceptions import DomainException


@dataclass(eq=False)
class SeoSettingsException(DomainException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с SEO настройками"


@dataclass(eq=False)
class PagePathEmptyException(SeoSettingsException):
    @property
    def message(self) -> str:
        return "Путь страницы не может быть пустым"


@dataclass(eq=False)
class PagePathInvalidException(SeoSettingsException):
    page_path: str

    @property
    def message(self) -> str:
        return f"Недопустимый путь страницы: {self.page_path}. Путь должен начинаться с '/'"


@dataclass(eq=False)
class PageNameEmptyException(SeoSettingsException):
    @property
    def message(self) -> str:
        return "Название страницы не может быть пустым"


@dataclass(eq=False)
class TitleEmptyException(SeoSettingsException):
    @property
    def message(self) -> str:
        return "Заголовок не может быть пустым"


@dataclass(eq=False)
class OgImageUrlInvalidException(SeoSettingsException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый URL OG изображения: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class CanonicalUrlInvalidException(SeoSettingsException):
    url: str

    @property
    def message(self) -> str:
        return f"Недопустимый канонический URL: {self.url}. URL должен начинаться с http:// или https://"


@dataclass(eq=False)
class SeoSettingsNotFoundException(SeoSettingsException):
    seo_settings_id: UUID

    @property
    def message(self) -> str:
        return f"SEO настройки с id {self.seo_settings_id} не найдены"


@dataclass(eq=False)
class SeoSettingsNotFoundByPathException(SeoSettingsException):
    page_path: str

    @property
    def message(self) -> str:
        return f"SEO настройки для пути '{self.page_path}' не найдены"


@dataclass(eq=False)
class SeoSettingsAlreadyExistsException(SeoSettingsException):
    page_path: str

    @property
    def message(self) -> str:
        return f"SEO настройки для пути '{self.page_path}' уже существуют"
