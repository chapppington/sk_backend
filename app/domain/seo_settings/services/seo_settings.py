from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.exceptions import (
    SeoSettingsAlreadyExistsException,
    SeoSettingsNotFoundByPathException,
    SeoSettingsNotFoundException,
)
from domain.seo_settings.interfaces.repository import BaseSeoSettingsRepository


@dataclass
class SeoSettingsService:
    seo_settings_repository: BaseSeoSettingsRepository

    async def create(
        self,
        seo_settings: SeoSettingsEntity,
    ) -> SeoSettingsEntity:
        page_path = seo_settings.page_path.as_generic_type()
        existing_settings = await self.seo_settings_repository.get_by_path(page_path)

        if existing_settings:
            raise SeoSettingsAlreadyExistsException(page_path=page_path)

        await self.seo_settings_repository.add(seo_settings)

        return seo_settings

    async def get_by_id(
        self,
        seo_settings_id: UUID,
    ) -> SeoSettingsEntity:
        seo_settings = await self.seo_settings_repository.get_by_id(seo_settings_id)

        if not seo_settings:
            raise SeoSettingsNotFoundException(seo_settings_id=seo_settings_id)

        return seo_settings

    async def get_by_path(
        self,
        page_path: str,
    ) -> SeoSettingsEntity:
        seo_settings = await self.seo_settings_repository.get_by_path(page_path)

        if not seo_settings:
            raise SeoSettingsNotFoundByPathException(page_path=page_path)

        return seo_settings

    async def update(
        self,
        seo_settings: SeoSettingsEntity,
    ) -> SeoSettingsEntity:
        existing_settings = await self.seo_settings_repository.get_by_id(seo_settings.oid)

        if not existing_settings:
            raise SeoSettingsNotFoundException(seo_settings_id=seo_settings.oid)

        current_path = existing_settings.page_path.as_generic_type()
        new_path = seo_settings.page_path.as_generic_type()

        if new_path != current_path:
            settings_with_path = await self.seo_settings_repository.get_by_path(new_path)

            if settings_with_path:
                raise SeoSettingsAlreadyExistsException(page_path=new_path)

        await self.seo_settings_repository.update(seo_settings)

        return seo_settings

    async def delete(
        self,
        seo_settings_id: UUID,
    ) -> None:
        await self.check_exists(seo_settings_id)
        await self.seo_settings_repository.delete(seo_settings_id)

    async def check_exists(
        self,
        seo_settings_id: UUID,
    ) -> None:
        await self.get_by_id(seo_settings_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> list[SeoSettingsEntity]:
        settings_iterable = self.seo_settings_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
            is_active=is_active,
        )
        return [settings async for settings in settings_iterable]

    async def count_many(
        self,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> int:
        return await self.seo_settings_repository.count_many(
            search=search,
            is_active=is_active,
        )
