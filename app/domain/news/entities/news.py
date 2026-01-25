from dataclasses import dataclass
from datetime import datetime

from domain.base.entity import BaseEntity
from domain.news.value_objects import (
    AltValueObject,
    CategoryValueObject,
    ContentValueObject,
    ImageUrlValueObject,
    ReadingTimeValueObject,
    ShortContentValueObject,
    SlugValueObject,
    TitleValueObject,
)


@dataclass(eq=False)
class NewsEntity(BaseEntity):
    category: CategoryValueObject
    title: TitleValueObject
    slug: SlugValueObject
    content: ContentValueObject
    short_content: ShortContentValueObject
    image_url: ImageUrlValueObject
    alt: AltValueObject
    reading_time: ReadingTimeValueObject
    date: datetime
