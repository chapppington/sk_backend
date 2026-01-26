from datetime import datetime
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
from application.news.commands import CreateNewsCommand
from presentation.api.v1.news.schemas import NewsRequestSchema


@pytest.mark.asyncio
async def test_get_news_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка новостей."""
    url = app.url_path_for("get_news_list")

    for _ in range(3):
        data = {
            "category": "События",
            "title": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "content": faker.text(max_nb_chars=1000),
            "short_content": faker.text(max_nb_chars=200),
            "image_url": faker.image_url(),
            "alt": faker.sentence(nb_words=3),
            "reading_time": faker.random_int(min=1, max=60),
            "date": datetime.now(),
        }
        request_schema = NewsRequestSchema(**data)
        await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))

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
async def test_get_news_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка новостей с пагинацией."""
    url = app.url_path_for("get_news_list")

    for _ in range(5):
        data = {
            "category": "События",
            "title": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "content": faker.text(max_nb_chars=1000),
            "short_content": faker.text(max_nb_chars=200),
            "image_url": faker.image_url(),
            "alt": faker.sentence(nb_words=3),
            "reading_time": faker.random_int(min=1, max=60),
            "date": datetime.now(),
        }
        request_schema = NewsRequestSchema(**data)
        await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_news_list_with_category_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка новостей с фильтром по категории."""
    url = app.url_path_for("get_news_list")

    for _ in range(3):
        data = {
            "category": "События",
            "title": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "content": faker.text(max_nb_chars=1000),
            "short_content": faker.text(max_nb_chars=200),
            "image_url": faker.image_url(),
            "alt": faker.sentence(nb_words=3),
            "reading_time": faker.random_int(min=1, max=60),
            "date": datetime.now(),
        }
        request_schema = NewsRequestSchema(**data)
        await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "category": "Полезное",
            "title": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "content": faker.text(max_nb_chars=1000),
            "short_content": faker.text(max_nb_chars=200),
            "image_url": faker.image_url(),
            "alt": faker.sentence(nb_words=3),
            "reading_time": faker.random_int(min=1, max=60),
            "date": datetime.now(),
        }
        request_schema = NewsRequestSchema(**data)
        await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"category": "События"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["category"] == "События" for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_news_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка новостей с поиском."""
    url = app.url_path_for("get_news_list")

    data1 = {
        "category": "События",
        "title": "Python programming tutorial",
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }
    request_schema1 = NewsRequestSchema(**data1)
    await mediator.handle_command(CreateNewsCommand(news=request_schema1.to_entity()))

    data2 = {
        "category": "События",
        "title": "JavaScript development guide",
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }
    request_schema2 = NewsRequestSchema(**data2)
    await mediator.handle_command(CreateNewsCommand(news=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"search": "Python"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Python" in json_response["data"]["items"][0]["title"]


@pytest.mark.asyncio
async def test_get_news_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения новости по ID."""
    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }

    request_schema = NewsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))
    news_id = result.oid

    url = app.url_path_for("get_news_by_id", news_id=news_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(news_id)
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["slug"] == data["slug"]


@pytest.mark.asyncio
async def test_get_news_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения новости по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_news_by_id", news_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_get_news_by_slug_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения новости по slug."""
    slug = faker.slug()
    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": slug,
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }

    request_schema = NewsRequestSchema(**data)
    await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))

    url = app.url_path_for("get_news_by_slug", slug=slug)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["slug"] == slug
    assert json_response["data"]["title"] == data["title"]


@pytest.mark.asyncio
async def test_get_news_by_slug_not_found(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест получения новости по несуществующему slug."""
    non_existent_slug = faker.slug()
    url = app.url_path_for("get_news_by_slug", slug=non_existent_slug)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_news_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания новости."""
    url = app.url_path_for("create_news")

    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now().isoformat(),
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["slug"] == data["slug"]
    assert json_response["data"]["category"] == data["category"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_news_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания новости без аутентификации."""
    url = app.url_path_for("create_news")

    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now().isoformat(),
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_news_duplicate_slug(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест создания новости с дублирующимся slug."""
    url = app.url_path_for("create_news")
    slug = faker.slug()

    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": slug,
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now().isoformat(),
    }

    request_schema = NewsRequestSchema(**data)
    await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.status_code == status.HTTP_409_CONFLICT
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_news_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления новости."""
    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }

    request_schema = NewsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))
    news_id = result.oid

    url = app.url_path_for("update_news", news_id=news_id)

    update_data = {
        "category": data["category"],
        "title": "Updated Title",
        "slug": faker.slug(),
        "content": data["content"],
        "short_content": data["short_content"],
        "image_url": data["image_url"],
        "alt": data["alt"],
        "reading_time": data["reading_time"],
        "date": datetime.now().isoformat(),
    }

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == "Updated Title"
    assert json_response["data"]["oid"] == str(news_id)


@pytest.mark.asyncio
async def test_update_news_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления новости без аутентификации."""
    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }

    request_schema = NewsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))
    news_id = result.oid

    url = app.url_path_for("update_news", news_id=news_id)

    api_data = {
        "category": data["category"],
        "title": data["title"],
        "slug": data["slug"],
        "content": data["content"],
        "short_content": data["short_content"],
        "image_url": data["image_url"],
        "alt": data["alt"],
        "reading_time": data["reading_time"],
        "date": datetime.now().isoformat(),
    }

    response: Response = client.put(url=url, json=api_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_news_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующей новости."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_news", news_id=non_existent_id)

    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now().isoformat(),
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_news_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления новости."""
    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }

    request_schema = NewsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))
    news_id = result.oid

    url = app.url_path_for("delete_news", news_id=news_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_news_by_id", news_id=news_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_news_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления новости без аутентификации."""
    data = {
        "category": "События",
        "title": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "content": faker.text(max_nb_chars=1000),
        "short_content": faker.text(max_nb_chars=200),
        "image_url": faker.image_url(),
        "alt": faker.sentence(nb_words=3),
        "reading_time": faker.random_int(min=1, max=60),
        "date": datetime.now(),
    }

    request_schema = NewsRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateNewsCommand(news=request_schema.to_entity()))
    news_id = result.oid

    url = app.url_path_for("delete_news", news_id=news_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_news_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующей новости."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_news", news_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
