from uuid import uuid4

import pytest
from faker import Faker

from application.mediator import Mediator
from application.seo_settings.commands import (
    CreateSeoSettingsCommand,
    UpdateSeoSettingsCommand,
)
from application.seo_settings.queries import GetSeoSettingsByIdQuery
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.exceptions.seo_settings import (
    SeoSettingsAlreadyExistsException,
    SeoSettingsNotFoundException,
)
from domain.seo_settings.value_objects import (
    PageNameValueObject,
    PagePathValueObject,
    TitleValueObject,
)


@pytest.mark.asyncio
async def test_update_seo_settings_command_success(
    mediator: Mediator,
    valid_seo_settings_entity: SeoSettingsEntity,
):
    create_command = CreateSeoSettingsCommand(seo_settings=valid_seo_settings_entity)
    create_result, *_ = await mediator.handle_command(create_command)
    created_settings: SeoSettingsEntity = create_result

    updated_settings = SeoSettingsEntity(
        page_path=created_settings.page_path,
        page_name=PageNameValueObject(value="Updated Page Name"),
        title=TitleValueObject(value="Updated Title"),
        description=created_settings.description,
    )

    update_command = UpdateSeoSettingsCommand(
        seo_settings_id=created_settings.oid,
        seo_settings=updated_settings,
    )
    update_result, *_ = await mediator.handle_command(update_command)

    updated: SeoSettingsEntity = update_result

    assert updated.oid == created_settings.oid
    assert updated.page_name.as_generic_type() == "Updated Page Name"
    assert updated.title.as_generic_type() == "Updated Title"
    assert updated.page_path.as_generic_type() == created_settings.page_path.as_generic_type()

    retrieved_settings = await mediator.handle_query(
        GetSeoSettingsByIdQuery(seo_settings_id=created_settings.oid),
    )

    assert retrieved_settings.page_name.as_generic_type() == "Updated Page Name"
    assert retrieved_settings.title.as_generic_type() == "Updated Title"


@pytest.mark.asyncio
async def test_update_seo_settings_command_not_found(
    mediator: Mediator,
    valid_seo_settings_entity: SeoSettingsEntity,
):
    non_existent_id = uuid4()
    update_command = UpdateSeoSettingsCommand(
        seo_settings_id=non_existent_id,
        seo_settings=valid_seo_settings_entity,
    )

    with pytest.raises(SeoSettingsNotFoundException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.seo_settings_id == non_existent_id


@pytest.mark.asyncio
async def test_update_seo_settings_command_duplicate_path(
    mediator: Mediator,
    valid_seo_settings_entity: SeoSettingsEntity,
    faker: Faker,
):
    settings1 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/page1"),
        page_name=PageNameValueObject(value=faker.sentence(nb_words=3)),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        description=valid_seo_settings_entity.description,
    )

    settings2 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/page2"),
        page_name=PageNameValueObject(value=faker.sentence(nb_words=3)),
        title=TitleValueObject(value=faker.sentence(nb_words=5)),
        description=valid_seo_settings_entity.description,
    )

    create_result1, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings1))
    created_settings1: SeoSettingsEntity = create_result1

    create_result2, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings2))
    created_settings2: SeoSettingsEntity = create_result2

    updated_settings = SeoSettingsEntity(
        page_path=created_settings2.page_path,
        page_name=created_settings1.page_name,
        title=created_settings1.title,
        description=created_settings1.description,
    )

    update_command = UpdateSeoSettingsCommand(
        seo_settings_id=created_settings1.oid,
        seo_settings=updated_settings,
    )

    with pytest.raises(SeoSettingsAlreadyExistsException) as exc_info:
        await mediator.handle_command(update_command)

    assert exc_info.value.page_path == created_settings2.page_path.as_generic_type()
