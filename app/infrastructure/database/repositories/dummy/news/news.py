from collections.abc import AsyncIterable
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from domain.news.entities.news import NewsEntity
from domain.news.interfaces.repository import BaseNewsRepository


@dataclass
class DummyInMemoryNewsRepository(BaseNewsRepository):
    _saved_news: list[NewsEntity] = field(default_factory=list, kw_only=True)

    async def add(self, news: NewsEntity) -> NewsEntity:
        self._saved_news.append(news)
        return news

    async def get_by_id(self, news_id: UUID) -> NewsEntity | None:
        try:
            return next(news for news in self._saved_news if news.oid == news_id)
        except StopIteration:
            return None

    async def get_by_slug(self, slug: str) -> NewsEntity | None:
        try:
            return next(news for news in self._saved_news if news.slug.as_generic_type() == slug)
        except StopIteration:
            return None

    async def update(self, news: NewsEntity) -> None:
        for i, saved_news in enumerate(self._saved_news):
            if saved_news.oid == news.oid:
                self._saved_news[i] = news
                return
        raise ValueError(f"News with id {news.oid} not found")

    async def delete(self, news_id: UUID) -> None:
        self._saved_news = [news for news in self._saved_news if news.oid != news_id]

    def _build_find_query(self, search: str | None = None, category: str | None = None) -> list[NewsEntity]:
        filtered_news = self._saved_news.copy()

        if category:
            filtered_news = [news for news in filtered_news if news.category.as_generic_type() == category]

        if search:
            search_lower = search.lower()
            filtered_news = [
                news
                for news in filtered_news
                if (
                    search_lower in news.title.as_generic_type().lower()
                    or search_lower in news.content.as_generic_type().lower()
                    or search_lower in news.short_content.as_generic_type().lower()
                    or search_lower in news.category.as_generic_type().lower()
                )
            ]

        return filtered_news

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        offset: int,
        limit: int,
        search: str | None = None,
        category: str | None = None,
    ) -> AsyncIterable[NewsEntity]:
        filtered_news = self._build_find_query(search, category)

        reverse = sort_order == -1

        if sort_field == "date":
            filtered_news.sort(key=lambda x: x.date, reverse=reverse)
        elif sort_field == "created_at":
            filtered_news.sort(key=lambda x: x.created_at, reverse=reverse)
        elif sort_field == "title":
            filtered_news.sort(key=lambda x: x.title.as_generic_type(), reverse=reverse)
        elif sort_field == "category":
            filtered_news.sort(key=lambda x: x.category.as_generic_type(), reverse=reverse)
        else:
            filtered_news.sort(key=lambda x: x.created_at, reverse=reverse)

        paginated_news = filtered_news[offset : offset + limit]

        for news in paginated_news:
            yield news

    async def count_many(self, search: str | None = None, category: str | None = None) -> int:
        filtered_news = self._build_find_query(search, category)
        return len(filtered_news)
