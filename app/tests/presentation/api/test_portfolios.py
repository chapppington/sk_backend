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
from application.portfolios.commands import CreatePortfolioCommand
from presentation.api.v1.portfolios.schemas import PortfolioRequestSchema


@pytest.mark.asyncio
async def test_get_portfolios_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка портфолио."""
    url = app.url_path_for("get_portfolios_list")

    for _ in range(3):
        data = {
            "name": faker.sentence(nb_words=3),
            "slug": faker.slug(),
            "poster": faker.image_url(),
            "poster_alt": faker.sentence(nb_words=3),
            "year": faker.random_int(min=2000, max=2100),
            "description": faker.text(max_nb_chars=1000),
            "task_title": faker.sentence(nb_words=5),
            "task_description": faker.text(max_nb_chars=500),
            "solution_title": faker.sentence(nb_words=5),
            "solution_description": faker.text(max_nb_chars=500),
            "solution_subtitle": faker.sentence(nb_words=3),
            "solution_subdescription": faker.text(max_nb_chars=300),
            "solution_image_left": faker.image_url(),
            "solution_image_left_alt": faker.sentence(nb_words=3),
            "solution_image_right": faker.image_url(),
            "solution_image_right_alt": faker.sentence(nb_words=3),
            "has_review": False,
        }
        request_schema = PortfolioRequestSchema(**data)
        await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))

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
async def test_get_portfolios_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка портфолио с пагинацией."""
    url = app.url_path_for("get_portfolios_list")

    for _ in range(5):
        data = {
            "name": faker.sentence(nb_words=3),
            "slug": faker.slug(),
            "poster": faker.image_url(),
            "poster_alt": faker.sentence(nb_words=3),
            "year": faker.random_int(min=2000, max=2100),
            "description": faker.text(max_nb_chars=1000),
            "task_title": faker.sentence(nb_words=5),
            "task_description": faker.text(max_nb_chars=500),
            "solution_title": faker.sentence(nb_words=5),
            "solution_description": faker.text(max_nb_chars=500),
            "solution_subtitle": faker.sentence(nb_words=3),
            "solution_subdescription": faker.text(max_nb_chars=300),
            "solution_image_left": faker.image_url(),
            "solution_image_left_alt": faker.sentence(nb_words=3),
            "solution_image_right": faker.image_url(),
            "solution_image_right_alt": faker.sentence(nb_words=3),
            "has_review": False,
        }
        request_schema = PortfolioRequestSchema(**data)
        await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_portfolios_list_with_year_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка портфолио с фильтром по году."""
    url = app.url_path_for("get_portfolios_list")

    for _ in range(3):
        data = {
            "name": faker.sentence(nb_words=3),
            "slug": faker.slug(),
            "poster": faker.image_url(),
            "poster_alt": faker.sentence(nb_words=3),
            "year": 2023,
            "description": faker.text(max_nb_chars=1000),
            "task_title": faker.sentence(nb_words=5),
            "task_description": faker.text(max_nb_chars=500),
            "solution_title": faker.sentence(nb_words=5),
            "solution_description": faker.text(max_nb_chars=500),
            "solution_subtitle": faker.sentence(nb_words=3),
            "solution_subdescription": faker.text(max_nb_chars=300),
            "solution_image_left": faker.image_url(),
            "solution_image_left_alt": faker.sentence(nb_words=3),
            "solution_image_right": faker.image_url(),
            "solution_image_right_alt": faker.sentence(nb_words=3),
            "has_review": False,
        }
        request_schema = PortfolioRequestSchema(**data)
        await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "name": faker.sentence(nb_words=3),
            "slug": faker.slug(),
            "poster": faker.image_url(),
            "poster_alt": faker.sentence(nb_words=3),
            "year": 2024,
            "description": faker.text(max_nb_chars=1000),
            "task_title": faker.sentence(nb_words=5),
            "task_description": faker.text(max_nb_chars=500),
            "solution_title": faker.sentence(nb_words=5),
            "solution_description": faker.text(max_nb_chars=500),
            "solution_subtitle": faker.sentence(nb_words=3),
            "solution_subdescription": faker.text(max_nb_chars=300),
            "solution_image_left": faker.image_url(),
            "solution_image_left_alt": faker.sentence(nb_words=3),
            "solution_image_right": faker.image_url(),
            "solution_image_right_alt": faker.sentence(nb_words=3),
            "has_review": False,
        }
        request_schema = PortfolioRequestSchema(**data)
        await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"year": 2023})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["year"] == 2023 for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_portfolios_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка портфолио с поиском."""
    url = app.url_path_for("get_portfolios_list")

    data1 = {
        "name": "Python Project",
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }
    request_schema1 = PortfolioRequestSchema(**data1)
    await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema1.to_entity()))

    data2 = {
        "name": "JavaScript Project",
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }
    request_schema2 = PortfolioRequestSchema(**data2)
    await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"search": "Python"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Python" in json_response["data"]["items"][0]["name"]


@pytest.mark.asyncio
async def test_get_portfolios_list_with_sorting(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка портфолио с сортировкой."""
    url = app.url_path_for("get_portfolios_list")

    data1 = {
        "name": "A Project",
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }
    request_schema1 = PortfolioRequestSchema(**data1)
    await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema1.to_entity()))

    data2 = {
        "name": "B Project",
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }
    request_schema2 = PortfolioRequestSchema(**data2)
    await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"sort_field": "name", "sort_order": 1})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["items"][0]["name"] < json_response["data"]["items"][1]["name"]


@pytest.mark.asyncio
async def test_get_portfolio_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения портфолио по ID."""
    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    request_schema = PortfolioRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))
    portfolio_id = result.oid

    url = app.url_path_for("get_portfolio_by_id", portfolio_id=portfolio_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(portfolio_id)
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["slug"] == data["slug"]


@pytest.mark.asyncio
async def test_get_portfolio_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения портфолио по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_portfolio_by_id", portfolio_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_get_portfolio_by_slug_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения портфолио по slug."""
    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    request_schema = PortfolioRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))
    slug = result.slug.as_generic_type()

    url = app.url_path_for("get_portfolio_by_slug", slug=slug)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["slug"] == slug
    assert json_response["data"]["name"] == data["name"]


@pytest.mark.asyncio
async def test_get_portfolio_by_slug_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения портфолио по несуществующему slug."""
    non_existent_slug = "non-existent-slug"
    url = app.url_path_for("get_portfolio_by_slug", slug=non_existent_slug)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_portfolio_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания портфолио."""
    url = app.url_path_for("create_portfolio")

    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["slug"] == data["slug"]
    assert json_response["data"]["year"] == data["year"]
    assert json_response["data"]["description"] == data["description"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_portfolio_with_review_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания портфолио с отзывом."""
    url = app.url_path_for("create_portfolio")

    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": True,
        "review_title": faker.sentence(nb_words=3),
        "review_text": faker.text(max_nb_chars=200),
        "review_name": faker.name(),
        "review_image": faker.image_url(),
        "review_role": faker.job(),
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["has_review"] is True
    assert json_response["data"]["review_title"] == data["review_title"]
    assert json_response["data"]["review_text"] == data["review_text"]
    assert json_response["data"]["review_name"] == data["review_name"]


@pytest.mark.asyncio
async def test_create_portfolio_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания портфолио без аутентификации."""
    url = app.url_path_for("create_portfolio")

    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_portfolio_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления портфолио."""
    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    request_schema = PortfolioRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))
    portfolio_id = result.oid

    url = app.url_path_for("update_portfolio", portfolio_id=portfolio_id)

    update_data = data.copy()
    update_data["name"] = "Updated Portfolio Name"
    update_data["year"] = 2025

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["name"] == "Updated Portfolio Name"
    assert json_response["data"]["year"] == 2025
    assert json_response["data"]["oid"] == str(portfolio_id)


@pytest.mark.asyncio
async def test_update_portfolio_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления портфолио без аутентификации."""
    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    request_schema = PortfolioRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))
    portfolio_id = result.oid

    url = app.url_path_for("update_portfolio", portfolio_id=portfolio_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_portfolio_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующего портфолио."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_portfolio", portfolio_id=non_existent_id)

    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_portfolio_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления портфолио."""
    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    request_schema = PortfolioRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))
    portfolio_id = result.oid

    url = app.url_path_for("delete_portfolio", portfolio_id=portfolio_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_portfolio_by_id", portfolio_id=portfolio_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_portfolio_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления портфолио без аутентификации."""
    data = {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "poster_alt": faker.sentence(nb_words=3),
        "year": faker.random_int(min=2000, max=2100),
        "description": faker.text(max_nb_chars=1000),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_left_alt": faker.sentence(nb_words=3),
        "solution_image_right": faker.image_url(),
        "solution_image_right_alt": faker.sentence(nb_words=3),
        "has_review": False,
    }

    request_schema = PortfolioRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreatePortfolioCommand(portfolio=request_schema.to_entity()))
    portfolio_id = result.oid

    url = app.url_path_for("delete_portfolio", portfolio_id=portfolio_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_portfolio_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующего портфолио."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_portfolio", portfolio_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
