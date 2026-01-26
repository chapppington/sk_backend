from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.news.entities import NewsEntity
from domain.news.exceptions import (
    NewsAlreadyExistsException,
    NewsNotFoundBySlugException,
    NewsNotFoundException,
)
from domain.news.interfaces.repository import BaseNewsRepository


@dataclass
class NewsService:
    news_repository: BaseNewsRepository

    async def create(
        self,
        news: NewsEntity,
    ) -> NewsEntity:
        slug = news.slug.as_generic_type()
        existing_news = await self.news_repository.get_by_slug(slug)

        if existing_news:
            raise NewsAlreadyExistsException(slug=slug)

        await self.news_repository.add(news)

        return news

    async def get_by_id(
        self,
        news_id: UUID,
    ) -> NewsEntity:
        news = await self.news_repository.get_by_id(news_id)

        if not news:
            raise NewsNotFoundException(news_id=news_id)

        return news

    async def get_by_slug(
        self,
        slug: str,
    ) -> NewsEntity:
        news = await self.news_repository.get_by_slug(slug)

        if not news:
            raise NewsNotFoundBySlugException(slug=slug)

        return news

    async def update(
        self,
        news: NewsEntity,
    ) -> NewsEntity:
        existing_news = await self.news_repository.get_by_id(news.oid)
        current_slug = existing_news.slug.as_generic_type()
        new_slug = news.slug.as_generic_type()

        if new_slug != current_slug:
            news_with_slug = await self.news_repository.get_by_slug(new_slug)

            if news_with_slug:
                raise NewsAlreadyExistsException(slug=new_slug)

        await self.news_repository.update(news)

        return news

    async def delete(
        self,
        news_id: UUID,
    ) -> None:
        await self.get_by_id(news_id)
        await self.news_repository.delete(news_id)

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        category: Optional[str] = None,
    ) -> list[NewsEntity]:
        news_iterable = self.news_repository.find_many(
            sort_field=sort_field,
            sort_order=sort_order,
            offset=offset,
            limit=limit,
            search=search,
            category=category,
        )
        return [news async for news in news_iterable]

    async def count_many(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
    ) -> int:
        return await self.news_repository.count_many(
            search=search,
            category=category,
        )
