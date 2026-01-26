from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.certificates.entities.sections import SectionEntity
from domain.certificates.exceptions.sections import (
    SectionAlreadyExistsException,
    SectionNotFoundException,
)
from domain.certificates.interfaces.repositories.sections import BaseSectionRepository


@dataclass
class SectionService:
    section_repository: BaseSectionRepository

    async def create(
        self,
        section: SectionEntity,
    ) -> SectionEntity:
        name = section.name.as_generic_type()
        existing_section = await self.section_repository.get_by_name(name)

        if existing_section:
            raise SectionAlreadyExistsException(name=name)

        await self.section_repository.add(section)

        return section

    async def get_by_id(
        self,
        section_id: UUID,
    ) -> SectionEntity:
        section = await self.section_repository.get_by_id(section_id)

        if not section:
            raise SectionNotFoundException(section_id=section_id)

        return section

    async def check_exists(
        self,
        section_id: UUID,
    ) -> None:
        await self.get_by_id(section_id)

    async def update(
        self,
        section: SectionEntity,
    ) -> SectionEntity:
        existing_section = await self.get_by_id(section.oid)
        current_name = existing_section.name.as_generic_type()
        new_name = section.name.as_generic_type()

        if new_name != current_name:
            existing_section = await self.section_repository.get_by_name(new_name)

            if existing_section and existing_section.oid != section.oid:
                raise SectionAlreadyExistsException(name=new_name)

        await self.section_repository.update(section)

        return section

    async def delete(
        self,
        section_id: UUID,
    ) -> None:
        await self.check_exists(section_id)
        await self.section_repository.delete(section_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
    ) -> list[SectionEntity]:
        sections_iterable = self.section_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
        )
        return [section async for section in sections_iterable]

    async def count_many(
        self,
        search: Optional[str] = None,
    ) -> int:
        return await self.section_repository.count_many(
            search=search,
        )
