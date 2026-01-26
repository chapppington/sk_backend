from uuid import uuid4

from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response

from application.mediator import Mediator
from application.seo_settings.commands import CreateSeoSettingsCommand
from presentation.api.v1.seo_settings.schemas import SeoSettingsRequestSchema


@pytest.mark.asyncio
async def test_get_seo_settings_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка SEO настроек."""
    url = app.url_path_for("get_seo_settings_list")

    for _ in range(3):
        data = {
            "page_path": f"/{faker.slug()}",
            "page_name": faker.sentence(nb_words=3),
            "title": faker.sentence(nb_words=5),
            "description": faker.text(max_nb_chars=500),
        }
        request_schema = SeoSettingsRequestSchema(**data)
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert "items" in json_response["data"]
    assert "pagination" in json_response["data"]
    assert len(json_response["data"]["items"]) == 3
    assert json_response["data"]["pagination"]["total"] == 3


@pytest.mark.asyncio
async def test_get_seo_settings_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка SEO настроек с пагинацией."""
    url = app.url_path_for("get_seo_settings_list")

    for _ in range(5):
        data = {
            "page_path": f"/{faker.slug()}",
            "page_name": faker.sentence(nb_words=3),
            "title": faker.sentence(nb_words=5),
            "description": faker.text(max_nb_chars=500),
        }
        request_schema = SeoSettingsRequestSchema(**data)
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_seo_settings_list_with_is_active_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка SEO настроек с фильтром по активности."""
    url = app.url_path_for("get_seo_settings_list")

    for _ in range(3):
        data = {
            "page_path": f"/{faker.slug()}",
            "page_name": faker.sentence(nb_words=3),
            "title": faker.sentence(nb_words=5),
            "description": faker.text(max_nb_chars=500),
            "is_active": True,
        }
        request_schema = SeoSettingsRequestSchema(**data)
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "page_path": f"/{faker.slug()}",
            "page_name": faker.sentence(nb_words=3),
            "title": faker.sentence(nb_words=5),
            "description": faker.text(max_nb_chars=500),
            "is_active": False,
        }
        request_schema = SeoSettingsRequestSchema(**data)
        await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"is_active": True})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["is_active"] is True for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_seo_settings_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка SEO настроек с поиском."""
    url = app.url_path_for("get_seo_settings_list")

    data1 = {
        "page_path": f"/{faker.slug()}",
        "page_name": "Home Page",
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }
    request_schema1 = SeoSettingsRequestSchema(**data1)
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema1.to_entity()))

    data2 = {
        "page_path": f"/{faker.slug()}",
        "page_name": "About Page",
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }
    request_schema2 = SeoSettingsRequestSchema(**data2)
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"search": "Home"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Home" in json_response["data"]["items"][0]["page_name"]


@pytest.mark.asyncio
async def test_get_seo_settings_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения SEO настроек по ID."""
    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))
    seo_settings_id = result.oid

    url = app.url_path_for("get_seo_settings_by_id", seo_settings_id=seo_settings_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(seo_settings_id)
    assert json_response["data"]["page_path"] == data["page_path"]
    assert json_response["data"]["page_name"] == data["page_name"]


@pytest.mark.asyncio
async def test_get_seo_settings_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения SEO настроек по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_seo_settings_by_id", seo_settings_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_get_seo_settings_by_path_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения SEO настроек по пути страницы."""
    page_path = f"/{faker.slug()}"
    data = {
        "page_path": page_path,
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))

    url = app.url_path_for("get_seo_settings_by_path", page_path=page_path)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["page_path"] == page_path
    assert json_response["data"]["page_name"] == data["page_name"]


@pytest.mark.asyncio
async def test_get_seo_settings_by_path_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения SEO настроек по несуществующему пути."""
    non_existent_path = "/non-existent-path"
    url = app.url_path_for("get_seo_settings_by_path", page_path=non_existent_path)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_seo_settings_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания SEO настроек."""
    url = app.url_path_for("create_seo_settings")

    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["page_path"] == data["page_path"]
    assert json_response["data"]["page_name"] == data["page_name"]
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["description"] == data["description"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_seo_settings_with_optional_fields_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания SEO настроек с опциональными полями."""
    url = app.url_path_for("create_seo_settings")

    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
        "keywords": faker.sentence(nb_words=5),
        "og_title": faker.sentence(nb_words=5),
        "og_description": faker.text(max_nb_chars=200),
        "og_image": faker.image_url(),
        "canonical_url": faker.url(),
        "is_active": True,
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["keywords"] == data["keywords"]
    assert json_response["data"]["og_title"] == data["og_title"]
    assert json_response["data"]["og_description"] == data["og_description"]
    assert json_response["data"]["og_image"] == data["og_image"]
    assert json_response["data"]["canonical_url"] == data["canonical_url"]
    assert json_response["data"]["is_active"] is True


@pytest.mark.asyncio
async def test_create_seo_settings_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания SEO настроек без аутентификации."""
    url = app.url_path_for("create_seo_settings")

    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_seo_settings_duplicate_path(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест создания SEO настроек с дублирующимся путем."""
    page_path = f"/{faker.slug()}"
    data = {
        "page_path": page_path,
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))

    url = app.url_path_for("create_seo_settings")

    duplicate_data = data.copy()
    duplicate_data["page_name"] = faker.sentence(nb_words=3)

    response: Response = authenticated_client.post(url=url, json=duplicate_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_seo_settings_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления SEO настроек."""
    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))
    seo_settings_id = result.oid

    url = app.url_path_for("update_seo_settings", seo_settings_id=seo_settings_id)

    update_data = data.copy()
    update_data["page_name"] = "Updated Page Name"
    update_data["title"] = "Updated Title"

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["page_name"] == "Updated Page Name"
    assert json_response["data"]["title"] == "Updated Title"
    assert json_response["data"]["oid"] == str(seo_settings_id)


@pytest.mark.asyncio
async def test_update_seo_settings_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления SEO настроек без аутентификации."""
    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))
    seo_settings_id = result.oid

    url = app.url_path_for("update_seo_settings", seo_settings_id=seo_settings_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_seo_settings_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующих SEO настроек."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_seo_settings", seo_settings_id=non_existent_id)

    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_seo_settings_duplicate_path(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления SEO настроек с дублирующимся путем."""
    page_path1 = f"/{faker.slug()}"
    page_path2 = f"/{faker.slug()}"

    data1 = {
        "page_path": page_path1,
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }
    request_schema1 = SeoSettingsRequestSchema(**data1)
    result1, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema1.to_entity()))

    data2 = {
        "page_path": page_path2,
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }
    request_schema2 = SeoSettingsRequestSchema(**data2)
    result2, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema2.to_entity()))

    url = app.url_path_for("update_seo_settings", seo_settings_id=result2.oid)

    update_data = data2.copy()
    update_data["page_path"] = page_path1

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_seo_settings_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления SEO настроек."""
    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))
    seo_settings_id = result.oid

    url = app.url_path_for("delete_seo_settings", seo_settings_id=seo_settings_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_seo_settings_by_id", seo_settings_id=seo_settings_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_seo_settings_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления SEO настроек без аутентификации."""
    data = {
        "page_path": f"/{faker.slug()}",
        "page_name": faker.sentence(nb_words=3),
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=500),
    }

    request_schema = SeoSettingsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateSeoSettingsCommand(seo_settings=request_schema.to_entity()))
    seo_settings_id = result.oid

    url = app.url_path_for("delete_seo_settings", seo_settings_id=seo_settings_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_seo_settings_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующих SEO настроек."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_seo_settings", seo_settings_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
