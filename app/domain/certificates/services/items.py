from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.certificates.entities.items import ItemEntity
from domain.certificates.exceptions.items import (
    ItemAlreadyExistsException,
    ItemNotFoundException,
)
from domain.certificates.interfaces.repositories.items import BaseItemRepository


@dataclass
class ItemService:
    item_repository: BaseItemRepository

    async def create(
        self,
        item: ItemEntity,
    ) -> ItemEntity:
        title = item.title.as_generic_type()
        section = item.section.as_generic_type()
        existing_item = await self.item_repository.get_by_title(title, section)

        if existing_item:
            raise ItemAlreadyExistsException(title=title)

        await self.item_repository.add(item)

        return item

    async def get_by_id(
        self,
        item_id: UUID,
    ) -> ItemEntity:
        item = await self.item_repository.get_by_id(item_id)

        if not item:
            raise ItemNotFoundException(item_id=item_id)

        return item

    async def check_exists(
        self,
        item_id: UUID,
    ) -> None:
        await self.get_by_id(item_id)

    async def update(
        self,
        item: ItemEntity,
    ) -> ItemEntity:
        existing_item = await self.get_by_id(item.oid)
        current_title = existing_item.title.as_generic_type()
        new_title = item.title.as_generic_type()

        if new_title != current_title:
            section = item.section.as_generic_type()
            existing_item = await self.item_repository.get_by_title(new_title, section)

            if existing_item and existing_item.oid != item.oid:
                raise ItemAlreadyExistsException(title=new_title)

        await self.item_repository.update(item)

        return item

    async def delete(
        self,
        item_id: UUID,
    ) -> None:
        await self.check_exists(item_id)
        await self.item_repository.delete(item_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        section: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> list[ItemEntity]:
        items_iterable = self.item_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
            section=section,
            is_active=is_active,
        )
        return [item async for item in items_iterable]

    async def count_many(
        self,
        search: Optional[str] = None,
        section: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> int:
        return await self.item_repository.count_many(
            search=search,
            section=section,
            is_active=is_active,
        )
