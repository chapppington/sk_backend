from dataclasses import dataclass

from domain.base.exceptions import ApplicationException


@dataclass(eq=False)
class MediaException(ApplicationException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при работе с медиа-файлами"


@dataclass(eq=False)
class MediaInvalidFilenameException(MediaException):
    @property
    def message(self) -> str:
        return "Для всех файлов должно быть указано имя"


@dataclass(eq=False)
class MediaInvalidExtensionException(MediaException):
    extension: str

    @property
    def message(self) -> str:
        return f"Файлы с расширением '{self.extension}' запрещены для загрузки"


@dataclass(eq=False)
class MediaInvalidContentTypeException(MediaException):
    content_type: str | None

    @property
    def message(self) -> str:
        return f"Тип содержимого '{self.content_type}' запрещен для загрузки"


@dataclass(eq=False)
class MediaEmptyFileException(MediaException):
    @property
    def message(self) -> str:
        return "Пустые файлы запрещены для загрузки"


@dataclass(eq=False)
class MediaFileTooLargeException(MediaException):
    @property
    def message(self) -> str:
        return "Размер файла превышает допустимый лимит"
