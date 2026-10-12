from abc import (
    ABC,
    abstractmethod,
)

from domain.catalog_texts.entities import CatalogTextEntity


class BaseCatalogTextRepository(ABC):
    @abstractmethod
    async def add(self, catalog_text: CatalogTextEntity) -> CatalogTextEntity: ...

    @abstractmethod
    async def get_by_category(self, category: str) -> CatalogTextEntity | None: ...

    @abstractmethod
    async def update(self, catalog_text: CatalogTextEntity) -> None: ...

    @abstractmethod
    async def find_all(self) -> list[CatalogTextEntity]: ...
