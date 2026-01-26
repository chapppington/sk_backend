from uuid import uuid4

import pytest

from application.mediator import Mediator
from application.seo_settings.commands import (
    CreateSeoSettingsCommand,
    DeleteSeoSettingsCommand,
)
from application.seo_settings.queries import GetSeoSettingsByIdQuery
from domain.seo_settings.exceptions.seo_settings import SeoSettingsNotFoundException


@pytest.mark.asyncio
async def test_delete_seo_settings_command_success(
    mediator: Mediator,
    valid_seo_settings_entity,
):
    create_result, *_ = await mediator.handle_command(
        CreateSeoSettingsCommand(seo_settings=valid_seo_settings_entity),
    )
    created_settings = create_result

    await mediator.handle_command(
        DeleteSeoSettingsCommand(seo_settings_id=created_settings.oid),
    )

    with pytest.raises(SeoSettingsNotFoundException):
        await mediator.handle_query(
            GetSeoSettingsByIdQuery(seo_settings_id=created_settings.oid),
        )


@pytest.mark.asyncio
async def test_delete_seo_settings_command_not_found(
    mediator: Mediator,
):
    non_existent_id = uuid4()

    with pytest.raises(SeoSettingsNotFoundException) as exc_info:
        await mediator.handle_command(
            DeleteSeoSettingsCommand(seo_settings_id=non_existent_id),
        )

    assert exc_info.value.seo_settings_id == non_existent_id
