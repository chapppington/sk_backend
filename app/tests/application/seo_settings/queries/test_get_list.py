import pytest
from faker import Faker

from application.mediator import Mediator
from application.seo_settings.commands import CreateSeoSettingsCommand
from application.seo_settings.queries import GetSeoSettingsListQuery
from domain.seo_settings.entities import SeoSettingsEntity
from domain.seo_settings.value_objects.seo_settings import (
    PageNameValueObject,
    PagePathValueObject,
    TitleValueObject,
)


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_success(mediator: Mediator, valid_seo_settings_entity):
    for i in range(5):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/page-{i}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    settings_list, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert len(settings_list) == 5
    assert total == 5
    assert all(isinstance(settings, SeoSettingsEntity) for settings in settings_list)


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_with_pagination(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    for i in range(5):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/page-{i}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    settings_list, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=2,
        ),
    )

    assert len(settings_list) == 2
    assert total == 5

    settings_list, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=2,
            limit=2,
        ),
    )

    assert len(settings_list) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_with_is_active_filter(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    for _ in range(3):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/active-{_}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
            is_active=True,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    for _ in range(2):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/inactive-{_}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
            is_active=False,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    settings_list, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            is_active=True,
        ),
    )

    assert len(settings_list) == 3
    assert total == 3
    assert all(settings.is_active is True for settings in settings_list)


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_with_search(
    mediator: Mediator,
    valid_seo_settings_entity,
    faker: Faker,
):
    settings1 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/python-page"),
        page_name=PageNameValueObject(value="Python Page"),
        title=TitleValueObject(value="Python programming"),
        description=valid_seo_settings_entity.description,
    )
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings1))

    settings2 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/javascript-page"),
        page_name=PageNameValueObject(value="JavaScript Page"),
        title=TitleValueObject(value="JavaScript development"),
        description=valid_seo_settings_entity.description,
    )
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings2))

    settings_list, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert len(settings_list) == 1
    assert total == 1
    assert "Python" in settings_list[0].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_with_sorting(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    settings1 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/first-page"),
        page_name=PageNameValueObject(value="First Page"),
        title=TitleValueObject(value="First Title"),
        description=valid_seo_settings_entity.description,
    )
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings1))

    settings2 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/second-page"),
        page_name=PageNameValueObject(value="Second Page"),
        title=TitleValueObject(value="Second Title"),
        description=valid_seo_settings_entity.description,
    )
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings2))

    settings_list, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="title",
            sort_order=1,
            offset=0,
            limit=10,
        ),
    )

    assert len(settings_list) == 2
    assert total == 2
    assert settings_list[0].title.as_generic_type() < settings_list[1].title.as_generic_type()


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_count_only(
    mediator: Mediator,
    valid_seo_settings_entity,
    faker: Faker,
):
    for i in range(3):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/count-page-{i}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    _, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_count_with_is_active(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    for _ in range(3):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/active-{_}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
            is_active=True,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    for _ in range(2):
        settings = SeoSettingsEntity(
            page_path=PagePathValueObject(value=f"/inactive-{_}"),
            page_name=valid_seo_settings_entity.page_name,
            title=valid_seo_settings_entity.title,
            description=valid_seo_settings_entity.description,
            is_active=False,
        )
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings))

    _, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            is_active=True,
        ),
    )

    assert total == 3


@pytest.mark.asyncio
async def test_get_seo_settings_list_query_count_with_search(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    settings1 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/python-tutorial"),
        page_name=PageNameValueObject(value="Python Tutorial"),
        title=TitleValueObject(value="Python tutorial"),
        description=valid_seo_settings_entity.description,
    )
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings1))

    settings2 = SeoSettingsEntity(
        page_path=PagePathValueObject(value="/javascript-guide"),
        page_name=PageNameValueObject(value="JavaScript Guide"),
        title=TitleValueObject(value="JavaScript guide"),
        description=valid_seo_settings_entity.description,
    )
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=settings2))

    _, total = await mediator.handle_query(
        GetSeoSettingsListQuery(
            sort_field="created_at",
            sort_order=-1,
            offset=0,
            limit=10,
            search="Python",
        ),
    )

    assert total == 1
