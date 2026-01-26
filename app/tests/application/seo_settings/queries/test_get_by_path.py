import pytest
from faker import Faker

from application.mediator import Mediator
from application.seo_settings.commands import CreateSeoSettingsCommand
from application.seo_settings.queries import GetSeoSettingsByPathQuery
from domain.seo_settings.exceptions.seo_settings import SeoSettingsNotFoundByPathException


@pytest.mark.asyncio
async def test_get_seo_settings_by_path_success(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    page_path = valid_seo_settings_entity.page_path.as_generic_type()

    await mediator.handle_command(
        CreateSeoSettingsCommand(seo_settings=valid_seo_settings_entity),
    )

    retrieved_settings = await mediator.handle_query(
        GetSeoSettingsByPathQuery(page_path=page_path),
    )

    assert retrieved_settings.page_path.as_generic_type() == page_path
    assert retrieved_settings.title.as_generic_type() == valid_seo_settings_entity.title.as_generic_type()


@pytest.mark.asyncio
async def test_get_seo_settings_by_path_not_found(
    mediator: Mediator,
    faker: Faker,
):
    non_existent_path = f"/{faker.slug()}"

    with pytest.raises(SeoSettingsNotFoundByPathException) as exc_info:
        await mediator.handle_query(
            GetSeoSettingsByPathQuery(page_path=non_existent_path),
        )

    assert exc_info.value.page_path == non_existent_path
