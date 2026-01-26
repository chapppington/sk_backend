import pytest
from faker import Faker

from application.mediator import Mediator
from application.seo_settings.commands import CreateSeoSettingsCommand
from application.seo_settings.queries import GetSeoSettingsByIdQuery
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.exceptions.seo_settings import SeoSettingsAlreadyExistsException
from domain.seo_settings.value_objects.seo_settings import (
    PageNameValueObject,
    TitleValueObject,
)


@pytest.mark.asyncio
async def test_create_seo_settings_command_success(
    mediator: Mediator,
    valid_seo_settings_entity: SeoSettingsEntity,
):
    command = CreateSeoSettingsCommand(seo_settings=valid_seo_settings_entity)
    result, *_ = await mediator.handle_command(command)

    seo_settings: SeoSettingsEntity = result

    assert seo_settings is not None
    assert seo_settings.page_path.as_generic_type() == valid_seo_settings_entity.page_path.as_generic_type()
    assert seo_settings.page_name.as_generic_type() == valid_seo_settings_entity.page_name.as_generic_type()
    assert seo_settings.title.as_generic_type() == valid_seo_settings_entity.title.as_generic_type()
    assert seo_settings.description.as_generic_type() == valid_seo_settings_entity.description.as_generic_type()
    assert seo_settings.oid is not None

    retrieved_settings = await mediator.handle_query(
        GetSeoSettingsByIdQuery(seo_settings_id=seo_settings.oid),
    )

    assert retrieved_settings.oid == seo_settings.oid
    assert retrieved_settings.page_path.as_generic_type() == valid_seo_settings_entity.page_path.as_generic_type()


@pytest.mark.asyncio
async def test_create_seo_settings_command_duplicate_path(
    mediator: Mediator,
    valid_seo_settings_entity: SeoSettingsEntity,
    faker: Faker,
):
    command = CreateSeoSettingsCommand(seo_settings=valid_seo_settings_entity)
    await mediator.handle_command(command)

    duplicate_settings = SeoSettingsEntity(
        page_path=valid_seo_settings_entity.page_path,
        page_name=PageNameValueObject(value=faker.sentence(nb_words=3)),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        description=valid_seo_settings_entity.description,
    )

    with pytest.raises(SeoSettingsAlreadyExistsException) as exc_info:
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=duplicate_settings))

    assert exc_info.value.page_path == valid_seo_settings_entity.page_path.as_generic_type()
