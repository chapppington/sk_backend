from dataclasses import dataclass
from typing import Optional

from domain.base.value_object import BaseValueObject
from domain.seo_settings.exceptions import (
    CanonicalUrlInvalidException,
    OgImageUrlInvalidException,
    PageNameEmptyException,
    PagePathEmptyException,
    PagePathInvalidException,
    TitleEmptyException,
)


@dataclass(frozen=True)
class PagePathValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise PagePathEmptyException()
        if not self.value.startswith("/"):
            raise PagePathInvalidException(page_path=self.value)
        if self.value != "/" and self.value.endswith("/"):
            raise PagePathInvalidException(page_path=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PageNameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise PageNameEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class TitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise TitleEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class DescriptionValueObject(BaseValueObject):
    value: str

    def validate(self):
        pass

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class KeywordsValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class OgTitleValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class OgDescriptionValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        pass

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class OgImageValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        if self.value and not self.value.startswith(("http://", "https://")):
            raise OgImageUrlInvalidException(url=self.value)

    def as_generic_type(self) -> Optional[str]:
        return self.value


@dataclass(frozen=True)
class CanonicalUrlValueObject(BaseValueObject):
    value: Optional[str]

    def validate(self):
        if self.value and not self.value.startswith(("http://", "https://")):
            raise CanonicalUrlInvalidException(url=self.value)

    def as_generic_type(self) -> Optional[str]:
        return self.value
