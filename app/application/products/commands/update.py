from dataclasses import (
    dataclass,
    field,
)
from typing import Optional
from uuid import UUID

from application.base.command import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.portfolios.services.portfolios import PortfolioService
from domain.products.entities import (
    AdvantageEntity,
    DetailedDescriptionEntity,
    DocumentationEntity,
    ImportantCharacteristicEntity,
    ImportantCharacteristicUnit,
    ProductEntity,
    SimpleDescriptionEntity,
)
from domain.products.services import ProductService
from domain.products.value_objects import (
    CategoryValueObject,
    DescriptionValueObject,
    NameValueObject,
    PreviewImageAltValueObject,
    PreviewImageUrlValueObject,
    SlugValueObject,
)


@dataclass(frozen=True)
class UpdateProductCommand(BaseCommand):
    product_id: UUID
    category: str
    name: str
    slug: str
    description: str
    preview_image_url: str
    preview_image_alt: Optional[str] = None
    important_characteristics: list[dict] = field(default_factory=list)
    advantages: list[dict] = field(default_factory=list)
    simple_description: list[dict] = field(default_factory=list)
    detailed_description: list[dict] = field(default_factory=list)
    documentation: list[dict] | None = None
    order: int = 0
    is_shown: bool = True
    show_advantages: bool = True
    portfolio_ids: list[UUID] = field(default_factory=list)


@dataclass(frozen=True)
class UpdateProductCommandHandler(
    BaseCommandHandler[UpdateProductCommand, ProductEntity],
):
    product_service: ProductService
    portfolio_service: PortfolioService

    async def handle(self, command: UpdateProductCommand) -> ProductEntity:
        existing_product = await self.product_service.get_by_id(command.product_id)

        if command.portfolio_ids:
            for portfolio_id in command.portfolio_ids:
                await self.portfolio_service.check_exists(portfolio_id)

        important_characteristics = []
        if command.important_characteristics:
            for char_data in command.important_characteristics:
                unit = None
                if char_data.get("unit"):
                    unit = ImportantCharacteristicUnit(text=char_data["unit"]["text"])
                important_characteristics.append(
                    ImportantCharacteristicEntity(
                        value=char_data["value"],
                        unit=unit,
                        description=char_data.get("description", ""),
                    ),
                )

        advantages = []
        if command.advantages:
            for adv_data in command.advantages:
                advantages.append(
                    AdvantageEntity(
                        label=adv_data["label"],
                        icon=adv_data["icon"],
                        image=adv_data.get("image"),
                        alt=adv_data.get("alt"),
                        description=adv_data.get("description", ""),
                    ),
                )

        simple_description = []
        if command.simple_description:
            simple_description = [
                SimpleDescriptionEntity(text=desc_data["text"]) for desc_data in command.simple_description
            ]

        detailed_description = []
        if command.detailed_description:
            detailed_description = [
                DetailedDescriptionEntity(title=desc_data["title"], description=desc_data["description"])
                for desc_data in command.detailed_description
            ]

        documentation = None
        if command.documentation:
            documentation = [
                DocumentationEntity(
                    title=doc_data["title"],
                    url=doc_data["url"],
                    type=doc_data["type"],
                )
                for doc_data in command.documentation
            ]

        product = ProductEntity(
            oid=existing_product.oid,
            created_at=existing_product.created_at,
            category=CategoryValueObject(value=command.category),
            name=NameValueObject(value=command.name),
            slug=SlugValueObject(value=command.slug),
            description=DescriptionValueObject(value=command.description),
            preview_image_url=PreviewImageUrlValueObject(value=command.preview_image_url),
            preview_image_alt=PreviewImageAltValueObject(value=command.preview_image_alt),
            important_characteristics=important_characteristics,
            advantages=advantages,
            simple_description=simple_description,
            detailed_description=detailed_description,
            documentation=documentation,
            order=command.order,
            is_shown=command.is_shown,
            show_advantages=command.show_advantages,
            portfolio_ids=command.portfolio_ids,
        )

        return await self.product_service.update(product)
