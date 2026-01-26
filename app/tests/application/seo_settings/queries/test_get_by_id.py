from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.seo_settings.commands import CreateSeoSettingsCommand
from application.seo_settings.queries import GetSeoSettingsByIdQuery
from domain.seo_settings.exceptions.seo_settings import SeoSettingsNotFoundException


@pytest.mark.asyncio
async def test_get_seo_settings_by_id_success(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    create_result, *_ = await mediator.handle_command(
        CreateSeoSettingsCommand(seo_settings=valid_seo_settings_entity),
    )
    created_settings = create_result

    retrieved_settings = await mediator.handle_query(
        GetSeoSettingsByIdQuery(seo_settings_id=created_settings.oid),
    )

    assert retrieved_settings.oid == created_settings.oid
    assert retrieved_settings.page_path.as_generic_type() == valid_seo_settings_entity.page_path.as_generic_type()
    assert retrieved_settings.page_name.as_generic_type() == valid_seo_settings_entity.page_name.as_generic_type()
    assert retrieved_settings.title.as_generic_type() == valid_seo_settings_entity.title.as_generic_type()


@pytest.mark.asyncio
async def test_get_seo_settings_by_id_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(SeoSettingsNotFoundException) as exc_info:
        await mediator.handle_query(
            GetSeoSettingsByIdQuery(seo_settings_id=non_existent_id),
        )

    assert exc_info.value.seo_settings_id == non_existent_id
